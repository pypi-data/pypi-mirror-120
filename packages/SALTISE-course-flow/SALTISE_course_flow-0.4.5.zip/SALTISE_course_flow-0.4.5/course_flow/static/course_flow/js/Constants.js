import * as React from "react";

export const node_keys=["activity","course","program"];
export const columnwidth = 160
export const nodewidth = 200;
export const node_ports={
    source:{
        e:[1,0.6],
        w:[0,0.6],
        s:[0.5,1]
    },
    target:{
        n:[0.5,0],
        e:[1,0.4],
        w:[0,0.4]
    }
}
export const port_keys=["n","e","s","w"];
export const port_direction=[
    [0,-1],
    [1,0],
    [0,1],
    [-1,0]
]
export const port_padding=10;
export const task_keys = {
    0:"",
    1:"research",
    2:"discuss",
    3:"problem",
    4:"analyze",
    5:"peerreview",
    6:"debate",
    7:"play",
    8:"create",
    9:"practice",
    10:"reading",
    11:"write",
    12:"present",
    13:"experiment",
    14:"quiz",
    15:"curation",
    16:"orchestration",
    17:"instrevaluate",
    18:"other",
    101:"jigsaw",
    102:"peer-instruction",
    103:"case-studies",
    104:"gallery-walk",
    105:"reflective-writing",
    106:"two-stage-exam",
    107:"toolkit",
    108:"one-minute-paper",
    109:"distributed-problem-solving",
    110:"peer-assessment"
}
export const context_keys = {
    0:"",
    1:"solo",
    2:"group",
    3:"class",
    101:"exercise",
    102:"test",
    103:"exam"
}
export const strategy_keys = {
    0:"",
    1:"jigsaw",
    2:"peer-instruction",
    3:"case-studies",
    4:"gallery-walk",
    5:"reflective-writing",
    6:"two-stage-exam",
    7:"toolkit",
    8:"one-minute-paper",
    9:"distributed-problem-solving",
    10:"peer-assessment",
    11:"other",
}
export const default_column_settings = {
    0:{colour:"#6738ff",icon:"other"},
    1:{colour:"#0b118a",icon:"ooci"},
    2:{colour:"#114cd4",icon:"home"},
    3:{colour:"#11b3d4",icon:"instruct"},
    4:{colour:"#04d07d",icon:"students"},
    10:{colour:"#6738ff",icon:"other"},
    11:{colour:"#ad351d",icon:"homework"},
    12:{colour:"#ed4a28",icon:"lesson"},
    13:{colour:"#ed8934",icon:"artifact"},
    14:{colour:"#f7ba2a",icon:"assessment"},
    20:{colour:"#369934",icon:"other"}
}
export const object_dictionary = {
    node:"node",
    week:"week",
    column:"column",
    outcome:"outcome",
    outcome_base:"outcome",
    workflow:"workflow"
}
export const parent_dictionary = {
    node:"week",
    week:"workflow",
    column:"workflow",
    outcome:"outcome",
    outcome_base:"workflow"
}
export const through_parent_dictionary = {
    node:"nodeweek",
    week:"weekworkflow",
    column:"columnworkflow",
    outcome:"outcomeoutcome",
    outcome_base:"outcomeworkflow"
}


//Get translate from an svg transform
export function getSVGTranslation(transform){
    var translate = transform.substring(transform.indexOf("translate(")+10, transform.indexOf(")")).split(",");
    return translate;
}

//Get the offset from the canvas of a specific jquery object
export function getCanvasOffset(node_dom){
    var node_offset = node_dom.offset();
    var canvas_offset = $(".workflow-canvas").offset();
    node_offset.left-=canvas_offset.left;
    node_offset.top-=canvas_offset.top;
    return node_offset;
}


//Check if the mouse event is within a box with the given padding around the element
export function mouseOutsidePadding(evt,elem,padding){
    if(elem.length==0) return true;
    let offset = elem.offset();
    let width = elem.outerWidth();
    let height = elem.outerHeight();
    return (evt.pageX<offset.left-padding || evt.pageY<offset.top-padding || evt.pageX>offset.left+width+padding || evt.pageY>offset.top+height+padding);
}


//A utility function to trigger an event on each element. This is used to avoid .trigger, which bubbles (we will be careful to only trigger events on the elements that need them)
export function triggerHandlerEach(trigger,eventname){
    return trigger.each((i,element)=>{$(element).triggerHandler(eventname);});
}


export function pushOrCreate(obj,index,value){
    if(obj[index])obj[index].push(value);
    else obj[index]=[value];
}

export function cantorPairing(k1,k2){
    return parseInt((k1+k2)*(k1+k2+1)/2+k2);
}

export function hasIntersection(list1,list2){
    return list1.filter(value=>list2.includes(value)).length>0;
}

//Gets intersection between two lists. Note that items appear in the same order as in list 1.
export function getIntersection(list1,list2){
    return list1.filter(value=>list2.includes(value));
}

//take a list of objects, then filter it based on which appear in the id list. The list is then resorted to match the order in the id list.
export function filterThenSortByID(object_list,id_list){
    return object_list.filter(obj=>id_list.includes(obj.id)).sort((a,b)=> id_list.indexOf(a.id)-id_list.indexOf(b.id));
}


export function getCompletionImg(completion_status,outcomes_type){
    if(outcomes_type==0 || completion_status & 1){
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

export class Loader{
    constructor(identifier){
        this.load_screen = $('<div></div>').appendTo(identifier).addClass('load-screen').on('click',(evt)=>{evt.preventDefault();});
    }
    
    endLoad(){
        this.load_screen.remove();
    }
}

