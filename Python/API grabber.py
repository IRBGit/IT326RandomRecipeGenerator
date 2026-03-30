import requests
def main():
    r=requests.get('https://www.themealdb.com/api/json/v1/1/list.php?i=list',)
    data = r.json()
    ingredients = [meal.get("strIngredient")+"\n" for meal in data.get("meals", [])]
    print(ingredients)
    with open("ingredients.txt", "w") as f:
          f.writelines(ingredients)
if __name__=="__main__":
        main()
    
