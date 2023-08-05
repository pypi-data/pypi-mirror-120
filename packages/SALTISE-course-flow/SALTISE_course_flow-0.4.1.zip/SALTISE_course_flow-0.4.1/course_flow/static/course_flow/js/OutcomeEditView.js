import * as React from "react";
import * as reactDom from "react-dom";
import {Provider, connect} from "react-redux";
import {ComponentJSON, OutcomeTitle} from "./ComponentJSON";
import OutcomeWorkflowView from "./OutcomeWorkflowView";
import {OutcomeBarOutcomeView, OutcomeBarOutcomeViewUnconnected} from "./OutcomeView";
import OutcomeView from "./OutcomeView";
import {getParentWorkflowByID,getParentOutcomeNodeByID, getOutcomeByID, getOutcomeOutcomeByID} from "./FindState";
import {WorkflowForMenu, renderMessageBox, closeMessageBox} from './MenuComponents';
import {newOutcome} from "./PostFunctions";
import {newOutcomeAction} from "./Reducers";

//Basic component representing the outcome view
class OutcomeEditView extends ComponentJSON{
    
    constructor(props){
        super(props);
        this.objectType="outcome";
    }
    
    render(){
        let data = this.props.data;
        var selector = this;
        
        let outcomes = data.outcomeworkflow_set.map(outcomeworkflow=>
            <OutcomeWorkflowView objectID={outcomeworkflow} parentID={data.id} renderer={this.props.renderer}/>
        ); 
            
        return(
            <div class="workflow-details">
                <div class="outcome-edit">
                    <h4>For This Workflow</h4>
                    {outcomes}
                    <button id="add-new-outcome" onClick={this.addNew.bind(this)}>Add new</button>
                    <ParentOutcomeBar/>
                </div>
            </div>
        );
    }
    
    
    addNew(){
        newOutcome(this.props.data.id,(response)=>{this.props.dispatch(newOutcomeAction(response))});
    }
    
}
const mapWorkflowStateToProps = state=>({
    data:state.workflow
})
export default connect(
    mapWorkflowStateToProps,
    null
)(OutcomeEditView)


class ParentOutcomeNodeViewUnconnected extends ComponentJSON{
    render(){
        let data = this.props.data;
        
        return(
            <div class="parent-outcome-node">
                {this.getContents(data.degree)}
                <ParentOutcomeView objectID={data.outcome} renderer={this.props.renderer}/>
            </div>
        )
        
    }
    
    getContents(completion_status){
        if(this.props.outcomes_type==0 || completion_status & 1){
            return (
                <img class="self-completed" src={iconpath+'solid_check.svg'}/>
            )
        }
        let contents=[];
        if(completion_status & 2){
            let divclass="";
            contents.push(
                <div class={"outcome-introduced outcome-degree"+divclass}>I</div>
            );
        }
        if(completion_status & 4){
            let divclass="";
            contents.push(
                <div class={"outcome-developed outcome-degree"+divclass}>D</div>
            );
        }
        if(completion_status & 8){
            let divclass="";
            contents.push(
                <div class={"outcome-advanced outcome-degree"+divclass}>A</div>
            );
        }
        return contents;
        
    }
}
const mapParentOutcomeNodeStateToProps = (state,own_props)=>(
    getParentOutcomeNodeByID(state,own_props.objectID)
)
export const ParentOutcomeNodeView = connect(
    mapParentOutcomeNodeStateToProps,
    null
)(ParentOutcomeNodeViewUnconnected)


class ParentOutcomeViewUnconnected extends OutcomeBarOutcomeViewUnconnected{
    render(){
        let data = this.props.data;
        let children = data.child_outcome_links.map((outcomeoutcome)=>
            <ParentOutcomeOutcomeView key={outcomeoutcome} objectID={outcomeoutcome} parentID={data.id} renderer={this.props.renderer} />
        );
                
        let dropIcon;
        if(this.state.is_dropped)dropIcon = "droptriangleup";
        else dropIcon = "droptriangledown";
        
        let droptext;
        if(this.state.is_dropped)droptext="hide";
        else droptext = "show "+children.length+" descendant"+((children.length>1&&"s")||"")
        
        
        return(
            <div
            class={
                "outcome"+((this.state.is_dropped && " dropped")||"")+" outcome-"+data.id
            }
            
            ref={this.maindiv}>
                <div class="outcome-title">
                    <OutcomeTitle data={this.props.data} titles={this.props.titles} rank={this.props.rank}/>
                </div>
                <input class="outcome-toggle-checkbox" type="checkbox" title="Toggle highlighting" onChange={this.clickFunction.bind(this)}/>
                {children.length>0 && 
                    <div class="outcome-drop" onClick={this.toggleDrop.bind(this)}>
                        <div class = "outcome-drop-img">
                            <img src={iconpath+dropIcon+".svg"}/>
                        </div>
                        <div class = "outcome-drop-text">
                            {droptext}
                        </div>
                    </div>
                }
                <div class="children-block" id={this.props.objectID+"-children-block"} ref={this.children_block}>
                    {children}
                </div>
            </div>
        )
    }
    
    
}
const mapParentOutcomeStateToProps = (state,own_props)=>(
    getOutcomeByID(state,own_props.objectID,"parent")
)
export const ParentOutcomeView = connect(
    mapParentOutcomeStateToProps,
    null
)(ParentOutcomeViewUnconnected)

class ParentOutcomeOutcomeViewUnconnected extends ComponentJSON{
    render(){
        let data = this.props.data;
        
        return (
            <div class="outcome-outcome" id={data.id} ref={this.maindiv}>
                <ParentOutcomeView objectID={data.child} parentID={this.props.parentID} throughParentID={data.id}/>
            </div>
        );
    }
}
const mapParentOutcomeOutcomeStateToProps = (state,own_props)=>(
    getOutcomeOutcomeByID(state,own_props.objectID,"parent")
)
export const ParentOutcomeOutcomeView = connect(
    mapParentOutcomeOutcomeStateToProps,
    null
)(ParentOutcomeOutcomeViewUnconnected)





class ParentWorkflowViewUnconnected extends ComponentJSON{
    render(){
        let data = this.props.data;
        let outcomeworkflows = data.outcomeworkflow_set.map(outcomeworkflow=>
            <OutcomeWorkflowView objectID={outcomeworkflow} renderer={this.props.renderer}/>
        );
        return (
            <div>
                <div>From parent workflow: {data.title}</div>
                <div>
                    {outcomeworkflows}
                </div>
            </div>
        )
    }
}
const mapParentWorkflowStateToProps = (state,own_props)=>(
    getParentWorkflowByID(state,own_props.objectID)
)
export const ParentWorkflowView = connect(
    mapParentWorkflowStateToProps,
    null
)(ParentWorkflowViewUnconnected)

class OutcomeBarUnconnected extends ComponentJSON{
    render(){
        let data = this.props.data;
        var outcomebaroutcomes = data.map((outcome)=>
            <OutcomeBarOutcomeView key={outcome.outcome} objectID={outcome.outcome}/>
        );
        
        
        return reactDom.createPortal(
            <div id="outcome-bar-workflow" class="right-panel-inner">
                <h4 class="drag-and-drop">Outcomes:</h4>
                <div class="outcome-bar-outcome-block">
                    {outcomebaroutcomes}
                </div>
                {!read_only &&
                    <button id="edit-outcomes-button" onClick={this.editOutcomesClick.bind(this)}>Edit Outcomes</button>
                }
            </div>
        ,$("#outcome-bar")[0]);
    }
    
    editOutcomesClick(){
        this.props.renderer.render($("#container"),"outcomeedit");
    }
    
}
const mapOutcomeBarStateToProps = state =>(
    {data:state.outcomeworkflow}
)
export const OutcomeBar = connect(
    mapOutcomeBarStateToProps,
    null
)(OutcomeBarUnconnected)


class ParentOutcomeBarUnconnected extends ComponentJSON{
    render(){
        let data = this.props.data;
        var outcomebaroutcomes = data.map((node)=>node.outcomenode_unique_set.map(outcomenode=>
            <ParentOutcomeNodeView key={outcomenode} objectID={outcomenode}/>
        ));
        
        
        return reactDom.createPortal(
            <div id="outcome-bar-workflow" class="right-panel-inner">
                <h4 class="drag-and-drop">From Parent Workflow:</h4>
                <div class="outcome-bar-outcome-block">
                    {outcomebaroutcomes}
                </div>
            </div>
        ,$("#outcome-bar")[0]);
    }
    
}
const mapParentOutcomeBarStateToProps = state =>(
    {data:state.parent_node}
)
export const ParentOutcomeBar = connect(
    mapParentOutcomeBarStateToProps,
    null
)(ParentOutcomeBarUnconnected)