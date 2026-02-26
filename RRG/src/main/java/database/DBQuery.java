package com.RRG.db;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class DBQuery 
{
    private DBConnect dbConnect;

    public DBQuery(DBConnect dbConnect)
    {
        this.dbConnect = dbConnect;
    }

    public ResultSet executeQuery(String sql, Object... params) throws SQLException
    {
        Connection conn = dbConnect.getConnection();
        PreparedStatement stmt = conn.prepareStatement((sql));

        for (int i = 0; i < params.length; i++)
        {
            stmt.setObject(i + 1, params[i]);
        }

        return stmt.executeQuery();
    }

    public int executeUpdate(String sql, Object... params) throws SQLException
    {
        Connection conn = dbConnect.getConnection();
        PreparedStatement stmt = conn.prepareStatement(sql);

        for (int i = 0; i < params.length; i++)
        {
            stmt.setObject(i + 1, params[i]);
        }


        return stmt.executeUpdate();
    }

    public void beginTransaction() throws SQLException
    {
        dbConnect.getConnection().setAutoCommit(false);
    }

    public void commitTransaction() throws SQLException
    {
        dbConnect.getConnection().commit();
        dbConnect.getConnection().setAutoCommit(true);
    }

    public void rollbackTransaction() throws SQLException
    {
        dbConnect.getConnection().rollback();
        dbConnect.getConnection().setAutoCommit(true);
    }
}
