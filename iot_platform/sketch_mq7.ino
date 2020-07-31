int GasPin = A0; // 가스센서 입력을 위한 아날로그 핀

void setup() {
pinMode(GasPin ,INPUT); // 아날로그 핀 A0를 입력모드로 설정
Serial.begin(9600);
}
void loop() {
Serial.println(analogRead(GasPin)); // 가스센서로부터 아날로 데이터를 받아와 시리얼 모니터로 출력함
delay(500); // 10ms 대기
}
