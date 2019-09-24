package com.mycompany.app;


import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPoolConfig;
import redis.clients.jedis.JedisSentinelPool;

public class TestRedisSentinel {
  public static void main(String[] args) {
    JedisPoolConfig config = new JedisPoolConfig();
    config.setMaxTotal(10);
    config.setMaxWaitMillis(1000);

    String masterName = "mymaster";
    String password = "redhat";

    Set<String> sentinelSet = new HashSet<String>();
    sentinelSet.add("192.168.175.101:26379");
    sentinelSet.add("192.168.175.102:26379");
    sentinelSet.add("192.168.175.103:26379");

    JedisSentinelPool pool = null;
    Jedis jedis = null;
    try {

      System.out.println("==============================start======================================");

      pool = new JedisSentinelPool(masterName, sentinelSet, config, password);
      jedis = pool.getResource();
      // jedis.auth(password);

      // https://www.cnblogs.com/sharpest/p/7879377.html
      Date currentTime = new Date();
      SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
      String dateString = formatter.format(currentTime);

      final String TEST_KEY = "test_key";
      final String TEST_VALUE = "TestRedisSentinel_" + dateString;

      jedis.set(TEST_KEY, TEST_VALUE);
      String value = jedis.get(TEST_KEY);

      System.out.println("set data: key(" + TEST_KEY + ")  ----->  value(" + TEST_VALUE + ")");
      System.out.println("get data: key(" + TEST_KEY + ")  ----->  value(" + value + ")");

      System.out.println("==============================end======================================");
    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      if (jedis != null) {
        jedis.close();

      }
      if (pool != null) {
        pool.close();
      }
    }
  }
}

