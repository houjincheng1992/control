var React = require('react');
var controlAjax = require("../common/labAjax");
var operation = require("../common/operation");

var aisModu = {
    params: {},
    platname: "modulate",
    preloadCondition: {
        currentCategory: '',
        currentPage: ''
    },
    actionListParam: {
        "owner": "",
        "action": "DescribeAISModu"
    },
    currentUser: {},
    init: function (currentCategory, currentPage, currentUser) {
        this.preloadCondition.currentCategory = currentCategory;
        this.preloadCondition.currentPage = currentPage;
        this.actionListParam.owner = currentUser.user.username;
        this.currentUser = currentUser;
    },
    LoadAISModu: function () {
        var params = {
            block: aisModu.preloadCondition.currentCategory.name
        };
        aisModu.initViewModel(params);
    },
    initViewModel: function (params) {
        var detailId = operation.getQueryString('detailId');
        if(detailId) {
            this.mode = 'detailId';
            var paramaisModu = {
                "owner": aisModu.actionListParam.owner,
                "action": "DescribeAISMode",
                sig_ids: [detailId]
            }
            controlAjax.doRequestByJsonStr("/api/", paramaisModu, function (result)){
                if(result.ret_code == 0){
                    this.initModuleViewModel(params, this.mode, result.ret_set[0]);
                }
            }.bind(this);
        }else{
            this.mode = 'overview';
            this.initModuleViewModel(params, this.mode);
        }
    },
    initBreadnav: function() {
        var Breadnav = React.createClass({
            displayName: 'breadnav',
            getInitState: function(){
                return {
                    detailId: false
                }
            },
            componentDidMount: function () {
                var detailId = operation.getQueryString("detailId");
                if (detailId) {
                    this.setState({detailId: detailId});
                }
            },
            returnTolist: function () {
                aisModu.preloadCondition.currentCategory.code = "aisModu";
                aisModu.preloadCondition.currentPage.code = "aismodu";
                this.locationPage();
            },
            refreshPage: function () {
                aisModu.preloadCondition.currentCategory.code = "aisModu";
                aisModu.preloadCondition.currentPage.code = "aisModu";
                this.locationPage(this.state.detailId);
            },
            locationPage: function (detailId) {
                var obj = aisModu;
                window.history.pushState(obj.preloadCondition.currentPage.code, null, "?id=" + obj.preloadCondition.currentPage.code + (detailId ? ("&detailId=" + detailId) : ''));
                obj.init(obj.preloadCondition.currentCategory, obj.preloadCondition.currentPage, obj.preloadCondition.currentUser);
            },
            render: function () {
                expandBreadnav = '';
                if (this.state.detailId) {
                    expandBreadnav = React.createElement("div", {className: "Breadnav"},
                        React.createElement("span", {className: "platform"}, this.props.platname),
                        React.createElement("span", {className: "to"}, ">"),
                        React.createElement("i", {className: "block", onClick: this.returnTolist}, this.props.block)),
                        React.createElement("span", {className: "to"}, ">"),
                        React.createElement("i", {className: "block", onClick: this.refreshPage}, this.props.block)
                } else {
                    expandBreadnav = React.createElement("div", {className: "Breadnav"},
                        React.createElement("span", {className: "platform"}, this.props.platname),
                        React.createElement("span", {className: "to"}, ">"),
                        React.createElement("i", {className: "block", onClick: this.returnTolist}, this.props.block)
                    )
                }
                return (
                    <div>
                    {expandBreadnav}
                    </div>
                )
            }
        });
        return Breadnav;
    },
    initModuleViewModel: function (params, mention, aismoduData) {
        var transMode = aisModu.mode;
        switch(mention){
            case "overview":
                var ViewModel = React.createClass({
                    displayName: 'viewModel',
                    getInitialState: function () {
                        return {

                        }
                    },
                    render: function () {
                        return (
                            <div className="contentBox">
                                <Breadnav block=>
                            </div>
                        )
                    }
                })
        }
    }
};
