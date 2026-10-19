#include "../extras/PortfolioPipeline/pipeline.h"
#include <cstdio>
int main() {
  const superjupiter::portfolio_example::Report r =
      superjupiter::portfolio_example::run();
  std::printf("%s: twenty components, %u observations, %u acknowledgements, "
              "%llu covered ms\n",
              r.passed ? "PASS" : "FAIL", r.observations, r.acknowledged,
              static_cast<unsigned long long>(r.integratedMs));
  return r.passed ? 0 : 1;
}
