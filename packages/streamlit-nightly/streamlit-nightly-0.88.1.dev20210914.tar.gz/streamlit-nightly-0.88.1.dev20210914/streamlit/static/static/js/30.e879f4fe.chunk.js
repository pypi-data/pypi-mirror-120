/*! For license information please see 30.e879f4fe.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[30],{3864:function(t,r,o){"use strict";o.r(r),o.d(r,"default",(function(){return u}));var e=o(11),a=(o(0),o(39)),n=o(188),c=o(3781),l=o.n(c),i=o(5);var u=Object(n.a)((function(t){var r=t.width,o=t.element,n=t.height,c=function(){return!!n},u=function(t){var l=JSON.parse(t.spec);c()?(l.layout.width=r,l.layout.height=n):o.useContainerWidth&&(l.layout.width=r);var i=Object(a.useTheme)();return l.layout=function(t,r){var o=r.colors,a=r.genericFonts,n={font:{color:o.bodyText,family:a.bodyFont},paper_bgcolor:o.bgColor,plot_bgcolor:o.secondaryBg};return Object(e.a)(Object(e.a)({},t),{},{font:Object(e.a)(Object(e.a)({},n.font),t.font),paper_bgcolor:t.paper_bgcolor||n.paper_bgcolor,plot_bgcolor:t.plot_bgcolor||n.plot_bgcolor})}(l.layout,i),l};switch(o.chart){case"url":return function(t){var o=n||450,e=r;return Object(i.jsx)("iframe",{title:"Plotly",src:t,style:{width:e,height:o}})}(o.url);case"figure":return function(t){var r=JSON.parse(t.config),o=u(t),e=o.data,a=o.layout,n=o.frames;return Object(i.jsx)(l.a,{className:"stPlotlyChart",data:e,layout:a,config:r,frames:n},c()?"fullscreen":"original")}(o.figure);default:throw new Error("Unrecognized PlotlyChart type: ".concat(o.chart))}}))}}]);