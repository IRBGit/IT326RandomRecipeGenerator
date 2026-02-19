package com.RRG.db;

import java.sql.ResultSet;
import java.sql.SQLException;

import com.RRG.model.*;

public class ObjectCreator 
{
    public User createUser(ResultSet rs) throws SQLException
    {
        return new User(
            rs.getInt("id"), 
            rs.getString("email"), 
            rs.getString("password")
        );
    }

    public Recipe createRecipe(ResultSet rs) throws SQLException
    {
        return new Recipe(
            rs.getInt("id"),
            rs.getString("name"),
            rs.getString("instructions")
        );
    }
}
