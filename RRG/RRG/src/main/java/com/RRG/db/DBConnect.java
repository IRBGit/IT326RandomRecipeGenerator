package com.RRG.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnect 
{
    private static final String URL = "";
    private static final String USERNAME = "";
    private static final String PASSWORD = "";

    private Connection connection;

    private void connect() throws SQLException
    {
        if (connection == null || connection.isClosed()) 
        {
            connection = DriverManager.getConnection(URL, USERNAME, PASSWORD);
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
        }
    }

    public boolean isConnected() throws SQLException
    {
        return (connection != null && !connection.isClosed());
    }    
}
