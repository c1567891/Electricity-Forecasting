# Electricity-Forecasting

使用台灣電力公司_過去電力供需資csv作為訓練資料,並對其Normalize使資料都介於0~1之間

使用台灣電力公司_本年度每日尖峰備轉容量率csv做為測試資料,同樣對其Normalize使資料都介於0~1之間

建立一個unit為4的一層LSTM,並加入一層的dense layer,且input size為(1,1)表示只看前一天的資訊去預測

訓練LSTM

將訓練好的LSTM去預測台灣電力公司_本年度每日尖峰備轉容量率得到答案

將答案寫入submission
