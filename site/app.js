import React, { Component } from "react";
import ReactDOM from "react-dom";

const Test = (message) => {
	return (
		<div>{message}</div>
	);
};

ReactDOM.render(
	<h1>Hello, world!</h1>,
	document.getElementById('root')
);

