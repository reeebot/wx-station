<!DOCTYPE html>
<html>
<head>
<title>hilltopWx</title>
<!--[if IE]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->

<style>

@import url("reset.css");

body {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 12px;
    color:#333
}

p {
    padding: 10px;
}

p1 {
    font-size: 74px;
}

p2 {
    font-size: 16px;
}

p3 {
    font-size: 14px;
}

p4 {
    font-size: 24px;
}

p5 {
    font-size: 46px;
    font-weight: bold;
}

p6 {
    font-size: 22px;
    font-weight: bold;
}

a:link {
    color: black;
}

/* visited link */
a:visited {
    color: black;
}

/* mouse over link */
a:hover {
    color: black;
}

/* selected link */
a:active {
    color: black;
}

a:link {
    text-decoration: none;
}

a:visited {
    text-decoration: none;
}

a:hover {
    text-decoration: none;
}

a:active {
    text-decoration: none;
}

#wrapper {
    width: 100%;
    min-width: 920px;
    margin: 0 auto;
}

#headerwrap {
    width: 922px;
    float: left;
    margin: 0 auto;
}

#header {
    height: 100px;
    background: #35CA60;
    border-radius: 4px;
    border: 2px solid #41B462;
    margin: 5px;
    text-align: center;
}

#contentliquid {
    float: left;
    width: 100%;
}

#contentwrap {
    margin-left: 660px;
    float: center;
}

#content {
    background: #cccccc;
    border-radius: 6px;
    border: 1px solid #ebebeb;
    margin: 5px;
    float: center;
    text-align: center;
    width: 250px;
    height: 484px;
}

#leftcolumnwrap {
    width: 655px;
    margin-left: -100%;
    float: left;
}

#leftcolumn {
    background: #000000;
    height: 480px;
    border-radius: 3px;
    border: 2px solid #000000;
    margin: 5px;
}

</style>


<script src="http://code.jquery.com/jquery-latest.js"></script>

<script>
 $(document).ready(function() {
   $("#wind").load("wind.php");
   var refreshId = setInterval(function() {
      $("#wind").load('wind.php');
   }, 5000);
   $.ajaxSetup({ cache: false });
});
</script>

<script>
 $(document).ready(function() {
 	 $("#livedata").load("temperature.php");
   var refreshId = setInterval(function() {
      $("#livedata").load('temperature.php');
   }, 5000);
   $.ajaxSetup({ cache: false });
});
</script>

<script>
var reimg
window.onload=function () {
  reimg=document.getElementById('re')
  setInterval(function () {
    reimg.src=reimg.src.replace(/\?.*/,function () {
      return '?'+new Date()
    })
  },5000)
}
</script>

</head>


<body>
    <div id="wrapper">
        
        <div id="headerwrap">
        <div id="header">
            <h1><a href="https://www.wunderground.com/personal-weather-station/dashboard?ID=KCOFORTC162">hilltopWx</a></h1><h3><i>5975'</i></h3>
        </div>
        </div>
        
        <div id="contentliquid">
        <div id="contentwrap">
        <div id="content">
            <div id="livedata"></div>
            <div id="wind"></div>
        </div>
        </div>
        </div>
        
        <div id="leftcolumnwrap">
        <div id="leftcolumn">
            <a href="/camerapics/live.jpg"><img src="/camerapics/live.jpg?" id="re" width="640" height="480"></a>
        </div>
        </div>

    </div>
</body>

</html>


