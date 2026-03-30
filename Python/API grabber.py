import requests
def createfile(text, filename):
      with open(filename+'.txt', 'w') as f:
            f.writelines(text)
def main():
    r=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?i=list',)
    data = r.json()
    ingredients = [meal.get("strIngredient")+"\n" for meal in data.get("meals", [])]
    createfile(ingredients, "ingredients")
    r=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?c=list',)
    data = r.json()
    categories = [meal.get("strCategory")+"\n" for meal in data.get("meals", [])]
    createfile(categories, "categories")
    r=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?a=list',)
    data = r.json()
    areas = [meal.get("strArea")+"\n" for meal in data.get("meals", [])]
    createfile(areas, "areas")
    
if __name__=="__main__":
        main()
    
