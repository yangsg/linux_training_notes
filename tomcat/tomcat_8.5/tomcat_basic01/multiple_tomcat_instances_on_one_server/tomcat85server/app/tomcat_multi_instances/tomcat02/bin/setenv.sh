#// 因为如果存在 $CATALINA_BASE/bin/setenv.sh, 则tomcat只会使用$CATALINA_BASE/bin/setenv.sh,
#// 而不再使用 $CATALINA_HOME/bin/setenv.sh, 所以如果要使用 $CATALINA_HOME/bin/setenv.sh
#// (比如设置多个tomcat实例公用的一些参数),
#// 需要手动调用 `source $CATALINA_HOME/bin/setenv.sh`
#// 详见： https://tomcat.apache.org/tomcat-8.5-doc/RUNNING.txt  或 less /app/apache-tomcat-8.5.39/RUNNING.txt
source $CATALINA_HOME/bin/setenv.sh

#export CATALINA_OPTS="$CATALINA_OPTS -Xms512m"
#export CATALINA_OPTS="$CATALINA_OPTS -Xmx1024m"

#//  注：java8已经不支持 -XX:PermSize 和 -XX:MaxPermSize 参数，所以设置了也会被ignore 掉
#// export CATALINA_OPTS="$CATALINA_OPTS -XX:PermSize=128m"
#// export CATALINA_OPTS="$CATALINA_OPTS -XX:MaxPermSize=512m"


#//      [root@tomcat85server ~]# java -XX:+PrintFlagsFinal -version | grep -iE 'HeapSize|PermSize|ThreadStackSize'
#//           intx CompilerThreadStackSize                   = 0                                   {pd product}
#//          uintx ErgoHeapSizeLimit                         = 0                                   {product}
#//          uintx HeapSizePerGCThread                       = 87241520                            {product}
#//          uintx InitialHeapSize                          := 16777216                            {product}
#//          uintx LargePageHeapSizeThreshold                = 134217728                           {product}
#//          uintx MaxHeapSize                              := 257949696                           {product}
#//           intx ThreadStackSize                           = 1024                                {pd product}
#//           intx VMThreadStackSize                         = 1024                                {pd product}
#//      java version "1.8.0_202"
#//      Java(TM) SE Runtime Environment (build 1.8.0_202-b08)
#//      Java HotSpot(TM) 64-Bit Server VM (build 25.202-b08, mixed mode)


#// Tomcat 调优及 JVM 参数优化  https://www.cnblogs.com/baihuitestsoftware/articles/6483690.html
#// Tomcat调优总结（Tomcat自身优化、Linux内核优化、JVM优化）  https://www.cnblogs.com/whx7762/p/9290242.html
#// https://www.mkyong.com/java/find-out-your-java-heap-memory-size/

#// 在线计算机单位换算工具：
#// https://cunchu.51240.com/
#// https://www.convert-me.com/en/convert/computer/








