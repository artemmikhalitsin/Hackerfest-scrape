$(function() {
	$("body").css("backgroundColor", "#111714");
});

var FormPane = React.createClass({
	getInitialState: function() {
		return {
			hasimg: false,
			value: "",
			profiles: []
		}
	},
	updated: function(event) {
		this.setState({
			value: event.target.value
		});

//		if(this.state.value == "reddit") {
//			this.setState({hasimg: true});
//		} else {
//			this.setState({hasimg: false});
//		}
	},
	onButtonClick: function() {
		console.log("Pressed");
		var old = this.state.profiles.slice();
		old.push(this.state.value);
		this.setState({
			profiles: old
		});
	},
	render: function() {
		if(this.state.value == "reddit") {
			$("body").animate({'backgroundColor': "#ff6600"}, 300);
			console.log("ok");
		}
		else {
			$("body").animate({"backgroundColor": "#112017"}, 200);
		}
		return (
			<div>
				<div className="formsection">
					<NiceForm onClick={this.onButtonClick} value={this.state.value} onChange={this.updated} img="fa fa-reddit" hasimg={this.state.hasimg} id="f1" bid="formb" /> 
					<h1>{this.state.value}</h1>
				</div>
				<ProfileListView profiles={this.state.profiles} />
			</div>
		);
	}
});

var NiceForm = React.createClass({
	render: function() {
		var jsx;
		if(this.props.hasimg) {
			console.log("oops");
			jsx = (
				<div className="niceform">
					<i className={this.props.img}></i> <input value={this.props.value} onChange={this.props.onChange} type="text"></input> <button id={this.props.bid} onClick={this.props.onClick}>Enter</button>
				</div>
			);
		}
		else {
			jsx = (
				<div className="niceform">
					<input value={this.props.value} onChange={this.props.onChange} type="text"></input> <button id={this.props.bid} onClick={this.props.onClick}>Enter</button>
				</div>
			);
		}
		return (
			jsx
		);
	}
});

var ProfileListView = React.createClass({
	render: function() {
		console.log(this.props.profiles);
		var listitems = this.props.profiles.map((profile) => <li>{profile}</li>);
		return (
			<div className="profilelistview">
				<ul>
					{listitems}
				</ul>
			</div>
		);
	}
});

ReactDOM.render(<FormPane />, document.getElementById("app"));
