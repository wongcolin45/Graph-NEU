'use client';

import ReactFlow, {
    Node, Edge, ReactFlowProvider,
    Background, BackgroundVariant,
    Controls, Panel,
    useReactFlow, MarkerType,
    useNodesState, useEdgesState,
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

export type CourseStatus = { satisfied: boolean; message: string; missing_groups: string[][]; };
export type CourseStatusMap = Map<string, CourseStatus>;


type LayoutDirection = 'LR' | 'TD';

const panelBtnStyle: React.CSSProperties = {
    background: '#fff',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '6px 12px',
    fontSize: '12px',
    fontWeight: 600,
    color: '#374151',
    cursor: 'pointer',
    boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
    marginBottom: '8px',
    marginRight: '8px',
};

const FlowCanvas = ({ nodes: initialNodes, edges: initialEdges, layout, onLayoutChange }: {
    nodes: Node[];
    edges: Edge[];
    layout: LayoutDirection;
    onLayoutChange: (l: LayoutDirection) => void;
}) => {
    const { fitView } = useReactFlow();
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, , onEdgesChange] = useEdgesState(initialEdges);

    useEffect(() => {
        setNodes(initialNodes);
        setTimeout(() => fitView({ padding: 0.15, duration: 400 }), 50);
    }, [initialNodes]);

    return (
        <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            nodesDraggable={true}
            panOnDrag={true}
            zoomOnScroll={true}
            zoomOnPinch={true}
            minZoom={0.05}
            maxZoom={3}
            proOptions={{ hideAttribution: true }}
            style={{ width: '100%', height: '100%' }}
        >
            <Background variant={BackgroundVariant.Dots} gap={28} size={1.2} color="#d1d5db" />
            <Controls showInteractive={false} />
            <Panel position="bottom-right">
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                    <div style={{ display: 'flex', gap: '6px', marginBottom: '8px', marginRight: '8px' }}>
                        <button
                            onClick={() => onLayoutChange('LR')}
                            title="Left-to-right layout"
                            style={{
                                ...panelBtnStyle,
                                marginBottom: 0, marginRight: 0,
                                background: layout === 'LR' ? '#eff6ff' : '#fff',
                                borderColor: layout === 'LR' ? '#93c5fd' : '#e5e7eb',
                                color: layout === 'LR' ? '#1d4ed8' : '#374151',
                            }}
                        >
                            → LR
                        </button>
                        <button
                            onClick={() => onLayoutChange('TD')}
                            title="Top-to-bottom layout"
                            style={{
                                ...panelBtnStyle,
                                marginBottom: 0, marginRight: 0,
                                background: layout === 'TD' ? '#eff6ff' : '#fff',
                                borderColor: layout === 'TD' ? '#93c5fd' : '#e5e7eb',
                                color: layout === 'TD' ? '#1d4ed8' : '#374151',
                            }}
                        >
                            ↓ TD
                        </button>
                    </div>
                    <button
                        onClick={() => fitView({ padding: 0.15, duration: 400 })}
                        title="Fit graph to screen"
                        style={panelBtnStyle}
                    >
                        Fit view
                    </button>
                </div>
            </Panel>
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
    const [layout, setLayout] = useState<LayoutDirection>('LR');
    const [graph, setGraph] = useState<{ nodes: Node[]; edges: Edge[] }>({ nodes: [], edges: [] });

    useEffect(() => {
        if (initialCourse) setSource(decodeURIComponent(initialCourse));
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
                    attributes,
                    layout,
                });
                setGraph(response.data);
            } catch (error) {
                console.error(error);
            }
        };
        updateGraph();
    }, [source, departments, minCourseID, maxCourseID, attributes, layout]);

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

        const styledNodes: Node[] = graph.nodes.map(node => ({
            ...node,
            type: 'graphNode',
            draggable: true,
            data: { ...node.data, courseStatusMap, layout },
        }));

        const styledEdges: Edge[] = graph.edges.map(edge => ({
            ...edge,
            type: 'graphEdge',
            markerEnd: { type: MarkerType.ArrowClosed, width: 18, height: 18 },
            data: { courseStatusMap }
        }));

        return (
            <ReactFlowProvider>
                <FlowCanvas nodes={styledNodes} edges={styledEdges} layout={layout} onLayoutChange={setLayout} />
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
