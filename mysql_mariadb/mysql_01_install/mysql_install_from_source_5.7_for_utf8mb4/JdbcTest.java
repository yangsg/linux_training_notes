package com.mycompany.app;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

// 代码 来自 如下 网址 并 稍作修改
//    https://yq.aliyun.com/articles/138488
// 参考:
//  https://www.runoob.com/java/java-mysql-connect.html
//  https://mathiasbynens.be/notes/mysql-utf8mb4
//  https://www.jianshu.com/p/f7d7609de6b0

/*
 * https://www.runoob.com/java/java-mysql-connect.html
 * MySQL 8.0 以上版本的数据库连接有所不同：
 *
 *     1、MySQL 8.0 以上版本驱动包版本 mysql-connector-java-8.0.16.jar。
 *
 *     2、com.mysql.jdbc.Driver 更换为 com.mysql.cj.jdbc.Driver。
 *
 *     MySQL 8.0 以上版本不需要建立 SSL 连接的，需要显示关闭。
 *
 *     最后还需要设置 CST。
 *
 */

public class JdbcTest
{
  // JDBC driver name and database URL
   static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
  //static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
  static final String DB_URL = "jdbc:mysql://192.168.175.30/test?useSSL=true";
  //static final String DB_URL = "jdbc:mysql://192.168.175.30/test?useUnicode=true&characterEncoding=UTF-8&useSSL=true";
  // 必要时 还 可以设置 connectionCollation=utf8mb4_unicode_ci 参数
  //static final String DB_URL = "jdbc:mysql://192.168.175.30/test?useUnicode=true&characterEncoding=UTF-8&connectionCollation=utf8mb4_unicode_ci";

  //  Database credentials
  static final String USER = "root";
  static final String PASS = "WWW.1.com";

  public static void main(String[] args) {
    Connection conn = null;
    Statement stmt = null;
    try{
      //STEP 2: Register JDBC driver
      Class.forName(JDBC_DRIVER);

      //STEP 3: Open a connection
      System.out.println("Connecting to a selected database...");
      conn = DriverManager.getConnection(DB_URL, USER, PASS);
      System.out.println("Connected database successfully...");

      //STEP 4: Execute a query
      System.out.println("Creating statement...");
      stmt = conn.createStatement();

      //String sql = " show variables like 'character%' ";
      String sql = " SHOW VARIABLES WHERE Variable_name LIKE 'character_set_%' OR Variable_name LIKE 'collation%' ";
      ResultSet rs = stmt.executeQuery(sql);
      //STEP 5: Extract data from result set
      while (rs.next()) {
        //Display values
        System.out.print(rs.getString(1));
        System.out.print("\t\t");
        System.out.print(rs.getString(2));

        System.out.println();
      }
      rs.close();
    }catch(SQLException se){
      //Handle errors for JDBC
      se.printStackTrace();
    }catch(Exception e){
      //Handle errors for Class.forName
      e.printStackTrace();
    }finally{
      //finally block used to close resources
      try{
        if(stmt!=null)
          conn.close();
      }catch(SQLException se){
        se.printStackTrace();
      }// do nothing
      try{
        if(conn!=null)
          conn.close();
      }catch(SQLException se){
        se.printStackTrace();
      }//end finally try
    }//end try
    System.out.println("Goodbye!");
  }//end main
}

