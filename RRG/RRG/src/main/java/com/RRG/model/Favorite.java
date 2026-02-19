package com.RRG.model;

import com.RRG.db.*;

public class Favorite 
{
    private int id;
    private int recipeID;
    private int userID;

    private Recipe item = null;

    public Favorite(int id, int recipe, int user, Recipe item)
    {
        this.id = id;
        this.recipeID = recipe;
        this.userID = user;
        this.item = item;
    }

    public Favorite(int id, int recipe, int user)
    {
        this.id = id;
        this.recipeID = recipe;
        this.userID = user;
    }

    public void setRecipe(Recipe item)
    {
        this.item = item;
    }

    public Recipe getRecipe()
    {
        return item;
    }
}
