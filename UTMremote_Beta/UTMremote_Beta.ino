// REMOTE:
#define blade_btn //button untuk menyalaka blade
#define capit_btn //button untuk menyalaka capit
#define activepump_btn //button untuk menyalaka pompa (kontraktror)
#define led_remote // led indikator remot

void setup() {
  // REMOTE:
  pinMode(blade_btn, INPUT);
  pinMode(capit_btn, INPUT);
  pinMode(activepump_btn, INPUT);
  pinMode(led_remote, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

}
