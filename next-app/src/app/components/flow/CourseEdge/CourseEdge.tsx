'use client';

import {BaseEdge, getSmoothStepPath, MarkerType} from 'reactflow';
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
                                                          sourceX, sourceY,
                                                          targetX, targetY, data}: any): JSX.Element => {

    const {courseStatusMap} = data;

    const coursesTaken = useUserDataStore((state) => state.coursesTaken);

    const [edgePath] = getSmoothStepPath({
        sourceX,
        sourceY,
        targetX,
        targetY,
        borderRadius: 6,
    });




    const getStyle = () => {
        const status: CourseStatus = courseStatusMap.get(target);
        const course = target.replace(/([a-zA-Z])(?=\d)/g, '$1 ');

        if (status == undefined) {
            return {}
        }

        if (status.satisfied) {
            if (coursesTaken.has(course)) {
                return { stroke: '#86efac', strokeWidth: 2 };
            }
            return { stroke: '#3b82f6', strokeWidth: 2 };
        }
        return { stroke: '#d1d5db', strokeDasharray: '5 4', strokeWidth: 1.5 };


    }


    return (
        <BaseEdge
            path={edgePath}
            markerEnd={MarkerType.ArrowClosed}
            style={getStyle()}
        />
    );
};

export default CourseEdge;
