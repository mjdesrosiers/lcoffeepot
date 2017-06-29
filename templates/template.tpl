
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Luna Coffee Pot Status</title>
	<!--[if lte IE 8]><script language="javascript" type="text/javascript" src="../../excanvas.min.js"></script><![endif]-->
	<script language="javascript" type="text/javascript" src="./scripts/jquery.js"></script>
	<script language="javascript" type="text/javascript" src="./scripts/jquery.flot.js"></script>
	<script language="javascript" type="text/javascript" src="./scripts/jquery.flot.time.js"></script>	
	<script type="text/javascript">

	$(function() {
		logcoffee = function() {
						console.log('asking for data')
						$.getJSON("coffee/data/", function (data) {
							var datalen = data['data'].length;
							console.log(datalen)
							var maxtime = data['data'][datalen-1][0];
							var mintime = data['data'][0][0];
							if ((maxtime - mintime) > (6 * 3600 * 1000)) {
								console.log('more than 6 hours of data!')
								mintime = maxtime - (6 * 3600 * 1000);
							}
							console.log("last time is:")
							console.log(maxtime)
							//console.log(data['data']);

							$.plot($("#placeholder"), [data['data']], {
								yaxis: {},
								xaxis: { mode: "time",
										 timeformat: "%h:%M %p",
										 min: mintime,
										 max: maxtime,
										 timezone: "browser",
										 minTickSize: [15, "minute"]
										}
								}
							);

						});
					};
		logcoffee();
		window.onload = function() {
			setInterval(logcoffee, 1000 * 60);
		}
	});

	</script>
</head>
<body>

	<div id="header">
		<h2>Coffee</h2>
	</div>

	<div id="content">

		<div class="demo-container">
			<div id="placeholder" class="demo-placeholder" style="width:100%;height:400px" ></div>
		</div>

	</div>

</body>
</html>
