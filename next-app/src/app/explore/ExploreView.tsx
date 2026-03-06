'use client';

import ReactFlow, {
    Node, Edge, ReactFlowProvider,
    Background, BackgroundVariant,
    Controls,
    useReactFlow,
} from 'reactflow';
import 'reactflow/dist/style.css';
import React, {JSX, useEffect, useState} from "react";
import '../globals.css';
import axios from 'axios';
import CourseNode from "@/app/components/flow/CourseNode/CourseNode";
import CourseEdge from "@/app/components/flow/CourseEdge/CourseEdge";
import Sidebar from "@/app/components/Sidebar/Sidebar";
import Loader from '@/app/components/Loader/Loader';
import useGraphStore from "@/app/store/useGraphStore";
import useUserDataStore from "@/app/store/useUserDataStore";
import {BASE_URL} from "@/app/api";
import useCourseFilterStore from "@/app/store/useCourseFilterStore";
import styles from './explore.module.css';


const nodeTypes = { graphNode: CourseNode };
const edgeTypes = { graphEdge: CourseEdge };

export type CourseStatus = { satisfied: boolean; message: string; };
export type CourseStatusMap = Map<string, CourseStatus>;


// Inner component — must live inside ReactFlowProvider to use useReactFlow
const FlowCanvas = ({
    nodes,
    edges,
}: {
    nodes: Node[];
    edges: Edge[];
}) => {
    const { fitView } = useReactFlow();

    useEffect(() => {
        if (!nodes.length) return;
        // Small delay lets ReactFlow finish its layout pass before fitting
        const id = setTimeout(() => fitView({ padding: 0.15, duration: 500 }), 60);
        return () => clearTimeout(id);
    }, [nodes]);

    return (
        <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            nodesDraggable={true}
            minZoom={0.1}
            maxZoom={2}
            proOptions={{ hideAttribution: true }}
            style={{ width: '100%', height: '100%' }}
        >
            <Background
                variant={BackgroundVariant.Dots}
                gap={28}
                size={1.2}
                color="#d1d5db"
            />
            <Controls showInteractive={false} />
        </ReactFlow>
    );
};


const ExploreView = ({ initialCourse }: { initialCourse?: string }): JSX.Element => {

    const source: string = useGraphStore((s) => s.source);
    const setSource = useGraphStore((s) => s.setSource);
    const coursesTaken = useUserDataStore((s) => s.coursesTaken);

    const departments: Set<string> = useCourseFilterStore((s) => s.departments);
    const minCourseID: number = useCourseFilterStore((s) => s.minCourseID);
    const maxCourseID: number = useCourseFilterStore((s) => s.maxCourseID);
    const attributes: string[] = useCourseFilterStore((s) => s.attributes);

    const [courseStatusMap, setCourseStatusMap] = useState<CourseStatusMap>(new Map());
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [graph, setGraph] = useState<{ nodes: Node[]; edges: Edge[] }>({ nodes: [], edges: [] });

    useEffect(() => {
        if (initialCourse) {
            setSource(decodeURIComponent(initialCourse));
        }
    }, [initialCourse]);

    useEffect(() => {
        const updateGraph = async () => {
            if (source === '') return;
            try {
                const url = `${BASE_URL}/api/graph/course/${source}`;
                const response = await axios.post(url, {
                    departments: Array.from(departments),
                    minCourseID,
                    maxCourseID,
                    attributes
                });
                setGraph(response.data);
            } catch (error) {
                console.error(error);
            }
        };
        updateGraph();
    }, [source, departments, minCourseID, maxCourseID, attributes]);

    useEffect(() => {
        const updateCourseStatusMap = async () => {
            if (!graph.nodes?.length) return;
            try {
                const courses = graph.nodes.map(node => node.data.course.replace(/\s+/g, ''));
                const url = `${BASE_URL}/api/course/check`;
                const response = await axios.post(url, {
                    coursesTaken: Array.from(coursesTaken),
                    courses
                });
                setCourseStatusMap(new Map(Object.entries(response.data)));
            } catch (error) {
                console.error(error);
            }
        };
        updateCourseStatusMap();
    }, [coursesTaken, graph]);


    const renderContents = (): JSX.Element => {
        if (source === '') {
            return (
                <div className={styles.emptyState}>
                    <svg viewBox="0 0 24 24" aria-hidden="true" className={styles.icon}>
                        <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18.4A8.4 8.4 0 1 1 20.4 12 8.41 8.41 0 0 1 12 20.4zm2.8-12.3-2.5 7.1-7.1 2.5 2.5-7.1 7.1-2.5z"/>
                    </svg>
                    <h2>Select a course to begin</h2>
                    <p className={styles.helpText}>
                        Use the sidebar search to choose a root&nbsp;course.<br/>
                        The prerequisite graph will appear here.
                    </p>
                </div>
            );
        }

        if (!graph.nodes?.length && !graph.edges?.length) {
            return <Loader/>;
        }

        const styledNodes: Node[] = graph.nodes.map((node) => ({
            ...node,
            type: 'graphNode',
            draggable: true,
            data: { ...node.data, courseStatusMap }
        }));

        const styledEdges: Edge[] = graph.edges.map((edge) => ({
            ...edge,
            type: 'graphEdge',
            data: { courseStatusMap }
        }));

        return (
            <ReactFlowProvider>
                <FlowCanvas nodes={styledNodes} edges={styledEdges} />
            </ReactFlowProvider>
        );
    };

    return (
        <div className={styles.exploreContainer}>
            {sidebarOpen && <Sidebar/>}
            <button
                className={styles.sidebarToggle}
                style={{ left: sidebarOpen ? '360px' : '0px' }}
                onClick={() => setSidebarOpen(prev => !prev)}
                aria-label={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
            >
                {sidebarOpen ? '‹' : '›'}
            </button>
            <div className={styles.explore}>
                {renderContents()}
            </div>
        </div>
    );
};

export default ExploreView;
