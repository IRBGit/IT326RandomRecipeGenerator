package com.RRG.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.ResultSet;
import java.sql.PreparedStatement;

import java.util.ArrayList;

public class Database
{
    private static final String URL = "";
    private static final String USERNAME = "";
    private static final String PASSWORD = "";

    private Connection connection;
    private boolean isConnected;

    private void connect() throws SQLException
    {
        if (connection == null || connection.isClosed()) 
        {
            connection = DriverManager.getConnection(URL, USERNAME, PASSWORD);
            if (connection != null && !connection.isClosed())
                isConnected = true;
            else isConnected = false;
        }
    }

    public Connection getConnection() throws SQLException
    {
        if (connection == null || connection.isClosed())
        {
            connect();
        }
        if (connection != null && !connection.isClosed())
            return connection;
        return null;
    }

    public void disconnect() throws SQLException
    {
        if (connection != null && !connection.isClosed())
        {
            connection.close();
            isConnected = false;
        }
    }

    public ResultSet executeQuery(PreparedStatement stmt) throws SQLException
    {
        // TODO
        return stmt.executeQuery();
    }

    public int executeUpdate(String query)
    {
        // TODO
        return 0;
    }

    public void beginTransaction()
    {
        // TODO
    }

    public void commitTransaction()
    {
        // TODO
    }

    public void rollbackTransaction()
    {
        // TODO
    }

    public boolean isConnected()
    {
        return isConnected;
    }
}