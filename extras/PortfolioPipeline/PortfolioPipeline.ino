// ESP32 recommended for this combined example. Synthetic RAM storage only.
#include "pipeline.h"
void setup() {
  Serial.begin(115200);
  const superjupiter::portfolio_example::Report r =
      superjupiter::portfolio_example::run();
  Serial.println(r.passed ? "PASS synthetic SuperJupiter portfolio pipeline"
                          : "FAIL synthetic SuperJupiter portfolio pipeline");
  Serial.println("Hardware validation pending.");
}
void loop() {}
