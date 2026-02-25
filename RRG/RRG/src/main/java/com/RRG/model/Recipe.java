package com.RRG.model;

import java.util.Map;

public class Recipe {
    private int id;
    private String name;
    private String category;
    private String area;
    private Map<String, Ingredient> ingredients;
    private String instructions;
    private String[] tags;
    private String video;

    public Recipe(int id, String name, String category, String area, Map<String, Ingredient> ingredients, String instructions, String[] tags, String video){
        id=this.id;
        name=this.name;
        category=this.category;
        area=this.area;
        ingredients=this.ingredients
        instructions=this.instructions
        tags=this.tags
        video=this.video
        
    }
}
