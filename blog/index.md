---
framework: lanyon
layout: main
onefile: False
mode: selfcontained
url: {lib: ../libraries}
---


<div class="container content">
  <div class="posts">
    {{# pages }}{{# date }}
    <div class="post">
      <h3 class="post-title">
      <a href="../{{ link }}">
        {{ title }}
      </a>
      </h3>
      <span class="post-date">{{ date }}</span>    
      {{ description }}
      


## testing site
The chunk below shows how to produce a simple scatter plot using Polychart library.





```r
return <- read.csv("C:/Users/Brian/Dropbox/Nathan (1)/Caine Investment Fund/pitch book latex/returnsformatted.csv", 
    h = T)
return$var2 <- as.numeric(as.POSIXct(paste0(return$var2, "-01-01")))
p4 <- Rickshaw$new()
p4$layer(var3 ~ var2, group = "var1", data = return, type = "stack", width = 560)
# add a helpful slider this easily; other features TRUE as a default
p4$set(slider = TRUE)
p4$print("chart6")
```


<div class='chart_container'>
  <div id='yAxischart6' class='yAxis'></div>
  <div id='chart6' class='rChart rickshaw'></div>
  <div id='legendchart6' class='legend'></div>
  <div id='sliderchart6' class='slider'></div>
</div>
<script type='text/javascript'> 
  var palette = new Rickshaw.Color.Palette({ scheme: "colorwheel" });
  var chartParams = {
 "dom": "chart6",
"width":            560,
"height":            400,
"scheme": "colorwheel",
"series": [
 {
 "data": [
 {
 "x":      915177600,
"y":          55.63 
},
{
 "x":      946713600,
"y":          41.47 
},
{
 "x":      978336000,
"y":          24.65 
},
{
 "x":     1009872000,
"y":           -2.9 
},
{
 "x":     1041408000,
"y":          24.96 
},
{
 "x":     1072944000,
"y":          38.56 
},
{
 "x":     1104566400,
"y":          45.36 
},
{
 "x":     1136102400,
"y":          68.31 
},
{
 "x":     1167638400,
"y":          77.55 
},
{
 "x":     1199174400,
"y":          11.86 
},
{
 "x":     1230796800,
"y":          41.46 
},
{
 "x":     1262332800,
"y":          62.76 
},
{
 "x":     1293868800,
"y":          66.18 
},
{
 "x":     1325404800,
"y":          92.76 
},
{
 "x":     1357027200,
"y":          155.2 
} 
],
"name": "aSP500",
"info": {
 "915177600": {
 "var1": "aSP500",
"var2":      915177600 
},
"946713600": {
 "var1": "aSP500",
"var2":      946713600 
},
"978336000": {
 "var1": "aSP500",
"var2":      978336000 
},
"1009872000": {
 "var1": "aSP500",
"var2":     1009872000 
},
"1041408000": {
 "var1": "aSP500",
"var2":     1041408000 
},
"1072944000": {
 "var1": "aSP500",
"var2":     1072944000 
},
"1104566400": {
 "var1": "aSP500",
"var2":     1104566400 
},
"1136102400": {
 "var1": "aSP500",
"var2":     1136102400 
},
"1167638400": {
 "var1": "aSP500",
"var2":     1167638400 
},
"1199174400": {
 "var1": "aSP500",
"var2":     1199174400 
},
"1230796800": {
 "var1": "aSP500",
"var2":     1230796800 
},
"1262332800": {
 "var1": "aSP500",
"var2":     1262332800 
},
"1293868800": {
 "var1": "aSP500",
"var2":     1293868800 
},
"1325404800": {
 "var1": "aSP500",
"var2":     1325404800 
},
"1357027200": {
 "var1": "aSP500",
"var2":     1357027200 
} 
},
"color":  palette.color()  
},
{
 "data": [
 {
 "x":      915177600,
"y":          64.33 
},
{
 "x":      946713600,
"y":         137.27 
},
{
 "x":      978336000,
"y":         182.89 
},
{
 "x":     1009872000,
"y":         166.29 
},
{
 "x":     1041408000,
"y":         223.49 
},
{
 "x":     1072944000,
"y":         230.83 
},
{
 "x":     1104566400,
"y":         254.71 
},
{
 "x":     1136102400,
"y":         305.97 
},
{
 "x":     1167638400,
"y":          272.6 
},
{
 "x":     1199174400,
"y":         103.89 
},
{
 "x":     1230796800,
"y":         177.18 
},
{
 "x":     1262332800,
"y":         244.62 
},
{
 "x":     1293868800,
"y":         246.93 
},
{
 "x":     1325404800,
"y":         260.36 
},
{
 "x":     1357027200,
"y":         317.11 
} 
],
"name": "Caine Fund",
"info": {
 "915177600": {
 "var1": "Caine Fund",
"var2":      915177600 
},
"946713600": {
 "var1": "Caine Fund",
"var2":      946713600 
},
"978336000": {
 "var1": "Caine Fund",
"var2":      978336000 
},
"1009872000": {
 "var1": "Caine Fund",
"var2":     1009872000 
},
"1041408000": {
 "var1": "Caine Fund",
"var2":     1041408000 
},
"1072944000": {
 "var1": "Caine Fund",
"var2":     1072944000 
},
"1104566400": {
 "var1": "Caine Fund",
"var2":     1104566400 
},
"1136102400": {
 "var1": "Caine Fund",
"var2":     1136102400 
},
"1167638400": {
 "var1": "Caine Fund",
"var2":     1167638400 
},
"1199174400": {
 "var1": "Caine Fund",
"var2":     1199174400 
},
"1230796800": {
 "var1": "Caine Fund",
"var2":     1230796800 
},
"1262332800": {
 "var1": "Caine Fund",
"var2":     1262332800 
},
"1293868800": {
 "var1": "Caine Fund",
"var2":     1293868800 
},
"1325404800": {
 "var1": "Caine Fund",
"var2":     1325404800 
},
"1357027200": {
 "var1": "Caine Fund",
"var2":     1357027200 
} 
},
"color":  palette.color()  
} 
],
"renderer": "stack",
"id": "chart6" 
}
  chartParams.element = document.querySelector('#chart6')
  
  var graphchart6 = new Rickshaw.Graph(chartParams);
  
  graphchart6.render();
  
  var xAxischart6 = new Rickshaw.Graph.Axis.Time({
 "graph":  graphchart6  
})
var yAxischart6 = new Rickshaw.Graph.Axis.Y({
 "graph":  graphchart6 ,
"orientation": "left",
"element":  document.getElementById('yAxischart6') ,
"tickFormat":  Rickshaw.Fixtures.Number.formatKMBT  
})
graphchart6.render()
var legendchart6 = new Rickshaw.Graph.Legend({
 "graph":  graphchart6 ,
"element":  document.getElementById('legendchart6')  
})
var shelvingchart6 = new Rickshaw.Graph.Behavior.Series.Toggle({
 "graph":  graphchart6 ,
"legend":  legendchart6  
})
var hoverDetailchart6 = new Rickshaw.Graph.HoverDetail({
 "graph":  graphchart6  
})
var highlightchart6 = new Rickshaw.Graph.Behavior.Series.Highlight({
 "graph":  graphchart6 ,
"legend":  legendchart6  
})
var sliderchart6 = new Rickshaw.Graph.RangeSlider({
 "graph":  graphchart6 ,
"element":  document.getElementById('sliderchart6')  
})
  
  graphchart6.render();
  
</script> 

```r
p4
```

<iframe src='
figure/unnamed-chunk-1.html
' scrolling='no' seamless
class='rChart rickshaw '
id=iframe-
chart6
></iframe>
<style>iframe.rChart{ width: 100%; height: 400px;}</style>


    </div>
    {{/ date }}{{/ pages }}
 </div>
</div>
