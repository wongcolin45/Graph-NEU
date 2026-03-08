'use client';

import {BaseEdge, getSmoothStepPath} from 'reactflow';
import {CourseStatus} from "@/app/explore/ExploreView";
import useUserDataStore from "@/app/store/useUserDataStore";

interface EdgeData {
    id: string;
    sourceX: any,
    sourceY: any,
    targetX: any,
    targetY: any,

}

const CourseEdge = ({id, source, target,
                                                          sourceX, sourceY, sourcePosition,
                                                          targetX, targetY, targetPosition,
                                                          markerEnd, data}: any): JSX.Element => {

    const {courseStatusMap} = data;

    const coursesTaken = useUserDataStore((state) => state.coursesTaken);

    const [edgePath] = getSmoothStepPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
        borderRadius: 8,
        offset: 24,
    });




    const getStyle = () => {
        const status: CourseStatus = courseStatusMap.get(target);
        const course = target.replace(/([a-zA-Z])(?=\d)/g, '$1 ');

        if (status == undefined) {
            return {}
        }

        if (status.satisfied) {
            if (coursesTaken.has(course)) {
                return { stroke: '#86efac', color: '#86efac', strokeWidth: 2 };
            }
            return { stroke: '#3b82f6', color: '#3b82f6', strokeWidth: 2 };
        }
        return { stroke: '#d1d5db', color: '#d1d5db', strokeDasharray: '5 4', strokeWidth: 1.5 };
    }


    return (
        <BaseEdge
            path={edgePath}
            markerEnd={markerEnd}
            style={getStyle()}
        />
    );
};

export default CourseEdge;
