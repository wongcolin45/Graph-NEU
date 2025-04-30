'use client';

import {BaseEdge, EdgeLabelRenderer, getBezierPath, MarkerType} from 'reactflow';
import {JSX} from "react";
import {CourseStatus} from "@/app/playground/page";

interface EdgeData {
    id: string;
    sourceX: any,
    sourceY: any,
    targetX: any,
    targetY: any,

}

const CourseEdge = ({id, source, target,
                                                          sourceX, sourceY,
                                                          targetX, targetY, data}: any): JSX.Element => {

    const {courseStatusMap, coursesTaken} = data;

    const [edgePath, labelX, labelY] = getBezierPath({
        sourceX,
        sourceY,
        targetX,
        targetY,
    });




    const getStyle = () => {
        const status: CourseStatus = courseStatusMap.get(target);
        const course = target.replace(/([a-zA-Z])(?=\d)/g, '$1 ');

        if (status == undefined) {
            return {}
        }

        if (status.satisfied) {
            if (coursesTaken.has(course)) {
                return {stroke: '#A9A9A9', strokeWidth: 1};
            }
            return {stroke: '#007bff', strokeWidth: 1};
        }
        return {stroke: 'gray', strokeDasharray: '5 5', strokeWidth: 1};


    }

    const markerEnd = {
        type: MarkerType.ArrowClosed,
        height: 50,
        width: 50,
        color: 'black'

    }

    return (
        <>
            <BaseEdge
                path={edgePath}
                markerEnd = {MarkerType.ArrowClosed}
                style={getStyle()}
            />
            <EdgeLabelRenderer>
              <div></div>
            </EdgeLabelRenderer>
        </>
    );
};

export default CourseEdge;
