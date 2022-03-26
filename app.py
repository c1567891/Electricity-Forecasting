if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--training',
                       default='台灣電力公司_過去電力供需資訊.csv',
                       help='input training data file name')

	parser.add_argument('--output',
                        default='submission.csv',
                        help='output file name')
	args = parser.parse_args()

	from turtle import shape
	import numpy as np
	from pandas import read_csv
	from keras.models import Sequential
	from keras.layers import Dense
	from keras.layers import LSTM
	from sklearn.preprocessing import MinMaxScaler
	from sklearn.metrics import mean_squared_error

	def createXY(dataset):
		dataX, dataY = [], []
		for i in range(len(dataset)-2):
			a = dataset[i:(i+1), 0]
			dataX.append(a)
			dataY.append(dataset[i + 1, 0])
		return np.array(dataX), np.array(dataY)

	# 載入訓練資料集
	train = read_csv('台灣電力公司_過去電力供需資訊.csv', usecols=[2])
	train = train.values
	train = train.astype('float32')
	# Normalize 資料
	scaler = MinMaxScaler(feature_range=(0, 1))
	train = scaler.fit_transform(train)
	# 載入測試資料集
	test = read_csv('本年度每日尖峰備轉容量率 (1).csv', usecols=[1])
	test = test.values
	test = test.astype('float32')
	# Normalize 資料
	scaler = MinMaxScaler(feature_range=(0, 1))
	test = scaler.fit_transform(test)

	trainX, trainY = createXY(train)

	trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
	test = np.reshape(test, (test.shape[0], 1, test.shape[1]))
	# 建立及訓練 LSTM 模型
	model = Sequential()
	model.add(LSTM(4, input_shape=(1, 1)))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)
	testPredict = model.predict(test)
	# 存放答案,前0~4為0325~0329
	ans=np.zeros(20)

	for i in range(len(ans)):
		if i == 0:
			b=model.predict(testPredict)
			ans[i]=b[82]
		else:
			b=model.predict(b)
			ans[i]=b[82]
	ans = scaler.inverse_transform([ans])
	import csv
	a=20220401
	# 寫入答案
	with open('submission.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['20220330', ans[0][5]])
		writer.writerow(['20220331', ans[0][6]])
		for i in range(13):
	  		writer.writerow([a+i, ans[0][7+i]])
