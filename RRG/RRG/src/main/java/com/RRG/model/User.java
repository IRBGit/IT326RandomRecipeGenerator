package com.RRG.model;

import java.util.ArrayList;

public class User {
    private int id;
    private String email;
    private String password;
    private ArrayList<Recipe> favorites;

    public User(int id, String email, String password)
    {
        this.id = id;
        this.email = email;
        this.password = password;
    }

    public String getEmail() { return email; }

    public boolean checkPassword(String password)
    {
        return this.password.equals(password);
    }
}
