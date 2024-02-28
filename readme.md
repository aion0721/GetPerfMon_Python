# GetPerfMon_Python

マシンの稼働統計情報を取得します

## 処理概要

CPU使用率、メモリ使用率、CPU温度を取得し、CSVファイルに書き込みます。

## 利用方法

```bash
# Default(output ./data | sleep 30)
hogehoge@piyopiyo:~/perfMon $ python main.py

# Set Args
hogehoge@piyopiyo:~/perfMon $ python main.py --output "/tmp/data.csv" --sleep 5
```

## 依存モジュール

特になし

## 前提

RaspberryPiでの実行を想定しています。

が別にどこでも動くと思います。



