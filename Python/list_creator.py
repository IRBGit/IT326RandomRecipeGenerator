import requests
import string
def createfile(text, filename):
      with open(filename+'.json', 'w') as f:
            f.writelines(text)
def main():
    # r=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?i=list',)
    # data = r.json()
    # ingredients = [meal.get("idIngredient") + " " + meal.get("strIngredient")+"\n" for meal in data.get("meals", [])]
    # createfile(ingredients, "ingredients")
    # r=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?c=list',)
    # data = r.json()
    # categories = [meal.get("strCategory")+"\n" for meal in data.get("meals", [])]
    # createfile(categories, "categories")
    # r=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?a=list',)
    # data = r.json()
    # areas = [meal.get("strArea")+"\n" for meal in data.get("meals", [])]
    # createfile(areas, "areas")
    for char in string.ascii_lowercase:
          r=requests.get('https://www.themealdb.com/api/json/v1/1/search.php?f='+char)
          data=r.text
          createfile(data, char+'_recipes' )
    for num in range(0,10):
        r=requests.get('https://www.themealdb.com/api/json/v1/1/search.php?f='+str(num))
        data=r.text
        createfile(data, str(num)+'_recipes' )
    
if __name__=="__main__":
        main()
    
