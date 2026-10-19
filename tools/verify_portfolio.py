#!/usr/bin/env python3
"""Verify the optional, exact-source twenty-component pipeline. No core service dependency."""
import argparse,hashlib,io,json,os,pathlib,shutil,subprocess,tempfile,urllib.request,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def run(*args,**kwargs):subprocess.run([str(a) for a in args],check=True,**kwargs)
def main():
 p=argparse.ArgumentParser();p.add_argument('--compiler',default='g++');p.add_argument('--source-root',type=pathlib.Path);args=p.parse_args()
 lock=json.loads((ROOT/'tools/portfolio-dependencies.json').read_text())
 sources=[]
 with tempfile.TemporaryDirectory(prefix='superjupiter-portfolio-') as temporary:
  work=pathlib.Path(temporary)
  for item in lock['dependencies']:
   if args.source_root:source=args.source_root/('superjupiter-'+item['slug'])
   else:
    assert item['repository']=='Super-Jupiter/superjupiter-'+item['slug']
    assert len(item['commit'])==40 and item['commit']!='0'*40 and all(ch in '0123456789abcdef' for ch in item['commit'])
    url='https://github.com/'+item['repository']+'/archive/'+item['commit']+'.zip'
    with urllib.request.urlopen(url,timeout=90) as response:data=response.read(5000001)
    assert len(data)<=5000000,'Archive too large'
    source=work/item['slug'];source.mkdir()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
     entries=[e for e in archive.infolist() if not e.is_dir()];assert len(entries)<500
     assert sum(e.file_size for e in entries)<=10000000,'Expanded archive too large'
     assert len({pathlib.PurePosixPath(e.filename).parts[0] for e in entries})==1,'Ambiguous archive root'
     for e in entries:
      path=pathlib.PurePosixPath(e.filename);assert not path.is_absolute() and '..' not in path.parts and '\\' not in e.filename
      assert (e.external_attr>>16)&0o170000!=0o120000,'Archive link rejected'
      relative=pathlib.Path(*path.parts[1:]);assert relative.parts and ':' not in str(relative)
      file=source/relative;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(archive.read(e))
   manifest=json.loads((source/'library.json').read_text())
   assert manifest['name']==item['package'] and manifest['version']==item['version'],'Dependency metadata mismatch'
   header=(source/'src'/(item['package']+'.h')).read_bytes().replace(b'\r\n',b'\n')
   assert hashlib.sha256(header).hexdigest()==item['headerSha256'],'Dependency header mismatch '+item['package']
   sources.append((item['name'],item['package'],source))
  sources.append(('SensorReplay','SuperJupiterSensorReplay',ROOT))
  flags=['-I'+str(source/'src') for _,_,source in sources]
  executable=work/'pipeline'
  run(args.compiler,'-std=c++11','-Wall','-Wextra','-Wconversion','-pedantic','-Werror','-fsanitize=address,undefined','-fno-omit-frame-pointer',*flags,ROOT/'tests/portfolio_integration.cpp','-o',executable)
  run(executable)
  cmake=work/'cmake-source';cmake.mkdir()
  common='cmake_minimum_required(VERSION 3.16)\nproject(SuperJupiterPortfolioConsumer LANGUAGES CXX)\n'
  cm=common
  for name,pkg,source in sources:
   # Component names have known explicit namespace spellings in the lock.
   item=next((i for i in lock['dependencies'] if i['name']==name),{'namespace':'sensor_replay'})
   prefix='SUPERJUPITER_'+item['namespace'].upper()
   cm+='set('+prefix+'_INSTALL ON CACHE BOOL "" FORCE)\n'
   cm+='add_subdirectory("'+source.as_posix()+'" "'+(work/('sub-'+name)).as_posix()+'")\n'
   cm+='if(TARGET superjupiter-'+item.get('slug','sensor-replay')+'-tests)\nmessage(FATAL_ERROR "Subproject developer tools leaked")\nendif()\n'
  tail='add_executable(portfolio "'+(ROOT/'tests/portfolio_integration.cpp').as_posix()+'")\ntarget_link_libraries(portfolio PRIVATE '+' '.join('SuperJupiter::'+name for name,_,_ in sources)+')\n'
  (cmake/'CMakeLists.txt').write_text(cm+tail)
  environment=dict(os.environ,CXX=args.compiler)
  build=work/'source-build';prefix=work/'installed'
  run('cmake','-S',cmake,'-B',build,'-DCMAKE_INSTALL_PREFIX='+str(prefix),env=environment)
  run('cmake','--build',build);run(build/'portfolio');run('cmake','--install',build)
  relocated=work/'relocated';shutil.move(str(prefix),relocated)
  installed=work/'installed-consumer';installed.mkdir()
  (installed/'CMakeLists.txt').write_text(common+''.join('find_package('+pkg+' CONFIG REQUIRED)\n' for _,pkg,_ in sources)+tail)
  consumerBuild=work/'consumer-build'
  run('cmake','-S',installed,'-B',consumerBuild,'-DCMAKE_PREFIX_PATH='+str(relocated),env=environment)
  run('cmake','--build',consumerBuild);run(consumerBuild/'portfolio')
 print('PASS: all twenty behaviours, source CMake targets and relocated installed CMake packages; hardware validation pending')
if __name__=='__main__':main()
