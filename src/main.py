from src import DataModel, CN_GetPage

if __name__ == '__main__':
    data=(CN_GetPage.GetAllinCent())
    # small test
    # data.extend(data)

    DataModel.IntoSqlite(data)
    print(data)