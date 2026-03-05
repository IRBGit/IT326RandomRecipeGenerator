package com.RRG.db;

import com.RRG.model.*;

import java.sql.*;
import java.util.*;

public class DatabaseModel 
{
    private DBConnect database;
    private DBQuery query;
    private ObjectCreator creator;

    public DatabaseModel()
    {
        this.database = new DBConnect();
        this.query = new DBQuery(database);
        this.creator = new ObjectCreator();
    }

    public boolean createUser(User user) throws SQLException
    {
        String sql = "INSERT INTO users (email, password) VALUES (?, ?)";

        return query.executeUpdate(sql, user.getEmail(), user.getPassword()) > 0;
    }

    public User getUserByEmail(String email) throws SQLException
    {
        String sql = "SELECT * FROM users WHERE email = ?";
        ResultSet rs = query.executeQuery(sql, email);

        if (rs.next())
        {
            return creator.createUser(rs);
        }
        return null;
    }

    public ArrayList<Recipe> searchRecipeByName(String name) throws SQLException
    {
        String sql = "SELECT * FROM recipes WHERE name LIKE ?";
        ResultSet rs = query.executeQuery(sql, "%" + name + "%");

        return creator.createRecipeList(rs);
    }

    public void saveFavorite(int userId, int recipeId) throws SQLException
    {
        String sql = "INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)";

        try (PreparedStatement stmt = database.getConnection().prepareStatement(sql))
        {
            stmt.setInt(1, userId);
            stmt.setInt(2, recipeId);
            stmt.executeUpdate();
        }
    }

    public void deleteFavorite(int userId, int recipeId) throws SQLException
    {
        String sql = "DELETE FROM favorites WHERE user_id = ? AND recipe_id = ?";

        try (PreparedStatement stmt = database.getConnection().prepareStatement(sql))
        {
            stmt.setInt(1, userId);
            stmt.setInt(2, recipeId);
            stmt.executeUpdate();
        }
    }

    public void addPersonalNote(int userId, int recipeId, String note) throws SQLException
    {
        String sql = "UPDATE favorites SET note = ? WHERE user_id = ? AND recipe_id = ?";

        try (PreparedStatement stmt = database.getConnection().prepareStatement(sql))
        {
            stmt.setString(1, note);
            stmt.setInt(2, userId);
            stmt.setInt(3, recipeId);
            stmt.executeUpdate();
        }
    }

    public void rateRecipe(int userID, int recipeId, int rating) throws SQLException
    {
        String sql = "INSERT INTO ratings (user_id, recipe_id, rating) VALUES (?, ?, ?) " + 
        "ON DUPLICATE KEY UPDATE rating = ?";

        try (PreparedStatement stmt = database.getConnection().prepareStatement(sql))
        {
            stmt.setInt(1, userID);
            stmt.setInt((2), recipeId);
            stmt.setInt(3, rating);
            stmt.setInt(4, rating);
            stmt.executeUpdate();
        }
    }

    public Favorite createFavorite(int favoriteID) throws SQLException
    {
        // TODO
        return new Favorite(0,0,0);
    }
}
