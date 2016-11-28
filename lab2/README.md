Author: Andrii Severin

Завдання роботи полягає у наступному:

1.Розробити схему бази даних на основі предметної галузі з ЛР№2-Ч1 у спосіб, що застосовується в СУБД MongoDB.
2.Розробити модуль роботи з базою даних на основі пакету PyMongo.
3.Реалізувати дві операції на вибір із використанням паралельної обробки даних Map/Reduce.
4.Реалізувати обчислення та виведення результату складного агрегативного запиту до бази даних з використанням функції aggregate() сервера MongoDB.

Тексти функції Map/Reduce та aggregate():
    def count_of_winPlayer(self):
        map = Code("""
    				   function(){
    					  var winner = this.winner;
    					  emit(winner, 1);
    		           };
    		           """)

        reduce = Code("""
    					  function(key, valuesPrices){
    						var sum = 0;
    						for (var i = 0; i < valuesPrices.length; i++) {
    						  sum += valuesPrices[i];
    						}
    						return sum;
    		              };
    		              """)
        results = self.competitions.map_reduce(map, reduce, "results_")
        for doc in results.find():
            print doc
        return results
    def count_by_year(self):
        map = Code("""
    				   function(){
    					  emit(this.tournament.year, 1);
    		           };
    		           """)

        reduce = Code("""
    					  function(key, valuesPrices){
    						var sum = 0;
    						for (var i = 0; i < valuesPrices.length; i++) {
    						  sum += valuesPrices[i];
    						}
    						return sum;
    		              };
    		              """)
        results = self.competitions.map_reduce(map, reduce, "result")
        res = results.find()
        for x in res:
            print x
        return results.find()

    def aggregationFunction(self):
        return self.competitions.aggregate([
            {"$group": {"_id": "$typeOfGame", "count":{"$sum": 1}, "messages": { "$push": {"message": "$date", "duration": "$duration"} }}},
            {"$sort": {"count": -1}}
        ])

