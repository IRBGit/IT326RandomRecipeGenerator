package com.RRG.db;

import com.RRG.model.*;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class DatabaseModel 
{
    private Database database;

    public DatabaseModel()
    {
        this.database = new Database();
    }

    public boolean createUser(User user) throws SQLException
    {
        String sql = "INSERT INTO users (email, password) VALUES (?, ?)";

        try (PreparedStatement stmt = database.getConnection().prepareStatement(sql))
        {
            stmt.setString(1, user.getEmail());
            stmt.setString(2, user.getPassword());
            return stmt.executeUpdate() > 0;
        }
    }

    public User getUserByEmail(String email) throws SQLException
    {
        String sql = "SELECT * FROM users WHERE email = ?";

        try (PreparedStatement stmt = database.getConnection().prepareStatement(sql))
        {
            stmt.setString(1, email);
            ResultSet rs = stmt.executeQuery();

            if (rs.next())
            {
                return new User(rs.getInt("id"), rs.getString("email"), rs.getString("password"));

            }
            return null;
        }
    }

    public List<Recipe> searchRecipeByName(String name) throws SQLException
    {
        List<Recipe> recipes = new ArrayList<>();
        String sql = "SELECT * FROM recipes WHERE name LIKE ?";

        try (PreparedStatement stmt = database.getConnection().prepareStatement(sql))
        {
            stmt.setString(1, "%" + name + "%");
            ResultSet rs = stmt.executeQuery();

            while (rs.next())
            {
                recipes.add(new Recipe(rs.getInt("id"), rs.getString("name")));
            }
        }

        return recipes;
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

        try (PreparedStatement stmt = database.getConnection().prepareStatement(sql)
        {
            stmt.setInt(1, userID);
            stmt.setInt((2), recipeId);
            stmt.setInt(3, rating);
            stmt.setInt(4, rating);
            stmt.executeUpdate();
        }
    }
}
