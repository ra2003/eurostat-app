function plotDataset(datasetId, datasetTitle, cachedir) {
	$('#chart-heading').text(datasetTitle);
    var embedCode = new Array(
      '<!-- Eurostat PEEE -->',
      '<iframe style="padding:0;margin:0;" height="100px" frameborder="0" width="100%" scrolling="no" src="http://eurostat.dev.okfn.org/embed?datasetId=' + datasetId + '"></iframe>',
      '<!-- /Eurostat PEEE -->'
	  );
	embedCode = embedCode.join(" \n ");
	$("#embed-code").val(embedCode);
	$.getJSON(cachedir + '/' + datasetId + '.json', null, plotItAll);
}

function plotItAll(jsondata) {
	data = {}
	$.each(jsondata.header.slice(1), function(idx, row) {
	timeCol = jsondata.header[0];
	seriesName = jsondata.header[idx+1];
	data[seriesName] = {
		label: seriesName,
		data: makeSeries(jsondata, timeCol, seriesName)
	};
	});
	var elem = $('#flot-chart');
	setupFlot(data, elem);
	doFlotPlot(data, elem);
}


/*****************************
  * Utils
  ****************************/


function makeSeries(tabular, firstColumnName, secondColumnName) {
	var idx1 = $.inArray(firstColumnName, tabular.header);
	var idx2 = $.inArray(secondColumnName, tabular.header);
	var series = [];
	$.each(tabular.data, function(i,row) {
		series.push([ row[idx1], row[idx2] ]);
	});
	return series;
}

function setupFlot(all_datasets, flotChart, options) {
	/*
	  Plot a set of datasets using flot.
	  
	  :param all_datasets: list of datasets. Should look like:
	  
	  "series-1": {
	  label: "Label 1",
	  data: [[1988, 483994], [1989, 479060]]
	  },		
	  "series-2": {
	  label: "Label 2",
	  data: [[1988, 218000], [1989, 203000]]
	  }
	*/
	// hard-code color indices to prevent them from shifting as
	// series are turned on/off
	var i = 0;
	$.each(all_datasets, function(key, val) {
		if(val.setid) {
			val.color=(val.setid-1);
		} else{
			val.color = i;
			++i;
		}
	});
	
	// setup checkboxes 
	var seriesList = flotChart.find(".flot-select-series");
	count = 0;
	var _inputList = $('<ul></ul>');
	var _tmpl = '<li><input type="checkbox" name="${key}" value="${key}" ${checked} ></input> ${label}</li>';
	for (var datasetKey in all_datasets) {
		if(count==0) {
			var _checked = 'checked=""';
		} else {
			var _checked = '';
		}
		var _templated = $.tmpl(_tmpl, {
			key: datasetKey,
			checked: _checked,
			label: all_datasets[datasetKey].label
			});
		_inputList.append(_templated)
		count = count + 1;
	}
	seriesList.html(_inputList);

	flotChart.find('.flot-chart-controls').find('input').live('click', function() {
		doFlotPlot(all_datasets, flotChart, options);
	});
	
	// setup charttype
	var chartType = "lines";
	var x = flotChart.find(".flot-chart-type").find("input[value="+chartType+"]");
	x.attr("checked", true);
}

function doFlotPlot(all_datasets, flotChart, options) {
	/*
	  :param options: optional set of options to be passed to flot plot.
	*/
	if (!options) {
		options = {};
	}

	// select datesets according to current state
	var datasets_to_plot = []
	var percent_flag = 0;
	flotChart.find(".flot-select-series").find("input:checked").each(function () {
		var key = $(this).attr("value");
		if (key) {
			if (all_datasets[key]) {
				datasets_to_plot.push(all_datasets[key]);
			}
		}
	});

	// yaxis percentage options
	if(percent_flag==1){
		options['yaxis'] = {
			tickFormatter: percentFormatter
		};
		options['y2axis'] = {};
	} else if(percent_flag==2){
		options['yaxis'] = {};
		options['y2axis'] = {
			tickFormatter: percentFormatter
		};
	} else{
		options['yaxis'] = {};
		options['y2axis'] = {};
	}


	// select plot type according to current state
	flotChart.find(".flot-chart-type").find("input:checked").each(function() {
		var value = $(this).attr("value");
		options[value] = { show: true };
	});

	var chartDiv = flotChart.find('.flot-chart')[0]; 
	$.plot(chartDiv, datasets_to_plot, options);
}

function percentFormatter(val, axis) {
	return (val * 100).toFixed(1) + " %";
}
