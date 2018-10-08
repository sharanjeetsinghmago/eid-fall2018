var sensorLib = require("node-dht-sensor");

var count = 0;

var t_max=0,t_min=100,t_avg=0,h_max=0,h_min=100,h_avg=0;

var sensor = {
	sensors: [ {
		        name: "Outdoor",
		        type: 22,
		        pin: 4
		} ],

	// Function to read sensor data
	
	read: function() {
		for (var a in this.sensors) 
		{	

			// Display Min, Max and Avg data after every 10 readings

			if(count == 10)
			{
				t_avg = t_avg/10;
				h_avg = h_avg/10;
				
				console.log("Temperture Max : " + t_max + "°C Min : " + t_min + "°C Avg : " + t_avg.toFixed(2) + "°C");
				console.log("Humidity   Max : " + h_max + "%  Min : " + h_min + "%  Avg : " + h_avg.toFixed(2) + "% ");

				t_max = 0;
				t_min = 100;
				t_avg = 0;
				h_max = 0;
				h_min = 100;
				h_avg = 0;

				count = 0;
			}
			
			// Displaying the current sensor readings

                	var b = sensorLib.read(this.sensors[a].type, this.sensors[a].pin);
                	console.log(this.sensors[a].name + ": " +
	              		b.temperature.toFixed(1) + "°C, " +
	              		b.humidity.toFixed(1) + "%");

			// Finding the Max Temp

			if(b.temperature.toFixed(1) > t_max)
				t_max = b.temperature.toFixed(1);
			
			// Finding the Min Temp

			if(b.temperature.toFixed(1) < t_min)
				t_min = b.temperature.toFixed(1);

			t_avg = t_avg + b.temperature;

			// Finding the Max Humidity

			if(b.humidity.toFixed(1) > h_max)
				h_max = b.humidity.toFixed(1);
			
			// Finding the Min Humidity

			if(b.humidity.toFixed(1) < h_min)
				h_min = b.humidity.toFixed(1);

			h_avg = h_avg + b.humidity;

			count++;
	    	}

		// Timer to read data after every 2 secs

            	setTimeout(function() {
                	sensor.read();
            		}, 2000);
        	}
};

sensor.read();
