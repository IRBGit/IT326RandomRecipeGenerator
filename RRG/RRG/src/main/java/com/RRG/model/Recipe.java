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
        this.id=id;
        this.name=name;
        this.category=category;
        this.area=area;
        this.ingredients=ingredients;
        this.instructions=instructions;
        this.tags=tags;
        this.video=video;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public String getArea() { return area; }
    public void setArea(String area) { this.area = area; }

    public Map<String, Ingredient> getIngredients() { return ingredients; }
    public void setIngredients(Map<String, Ingredient> ingredients) { this.ingredients = ingredients; }

    public String getInstructions() { return instructions; }
    public void setInstructions(String instructions) { this.instructions = instructions; }

    public String[] getTags() { return tags; }
    public void setTags(String[] tags) { this.tags = tags; }

    public String getVideo() { return video; }
    public void setVideo(String video) { this.video = video; }
}
