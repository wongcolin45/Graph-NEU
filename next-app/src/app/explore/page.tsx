'use client';

import ReactFlow, {Node, Edge, MarkerType, ReactFlowProvider} from 'reactflow';
import 'reactflow/dist/style.css';
import React, {JSX, useEffect, useState} from "react";
import '../globals.css';
import axios from 'axios';
import CourseNode from "@/app/components/flow/CourseNode/CourseNode";
import CourseEdge from "@/app/components/flow/CourseEdge/CourseEdge";
import styles from './playground.module.css'
import Loader from '@/app/components/Loader/Loader';
import useSidebarStore from "@/app/store/useSidebarStore";
import useGraphStore from "@/app/store/useGraphStore";
import useUserDataStore from "@/app/store/useUserDataStore";

const nodeTypes = {
  graphNode: CourseNode
};

const edgeTypes = {
  graphEdge: CourseEdge,
};

const BASE_URL: string = 'http://localhost:8000';

export type CourseStatus = {
  satisfied: boolean;
  message: string;
};

export type CourseStatusMap = Map<string, CourseStatus>;


const Explore = (): JSX.Element  => {

  // Zustand Shared State
  const toggleSidebar = useSidebarStore((s) => s.toggleSidebar);
  const source: string = useGraphStore((s) => s.source);
  const coursesTaken = useUserDataStore((s) => s.coursesTaken);


  // const [coursesTaken, setCoursesTaken] = useState(new Set());

  const [courseStatusMap, setCourseStatusMap] = useState<CourseStatusMap>(new Map());

  const [graph, setGraph] = useState<{
    nodes: Node[];
    edges: Edge[];
  }>({ nodes: [], edges: [] });

  useEffect(() => {
    const updateGraph: () => void = async () => {
      if (source === '') return;
      try {
        const url = `${BASE_URL}/api/graph/course/${source}`;
        const response = await axios.get(url);
        setGraph(response.data);
      } catch (error) {
        console.error(error);
      }
    }
    updateGraph()
  },[source])

  useEffect(() => {
    const updateCourseStatusMap = async () => {
      if (graph.nodes === undefined) {
        return;
      }
      try {
        const courses = graph.nodes.map(node => node.data.course.replace(/\s+/g, ''));
        console.log('Courses taken: '+Array.from(coursesTaken));
        const url = `${BASE_URL}/api/course/check`;
        const response = await axios.post(url, {
          coursesTaken: Array.from(coursesTaken),
          courses: courses
        });

        setCourseStatusMap(new Map(Object.entries(response.data)));
      } catch (error) {
        console.error(error);
      }
    }
    updateCourseStatusMap();
  }, [coursesTaken, graph]);

  const renderContents = (): JSX.Element => {
    if (graph.nodes === undefined || graph.nodes.length === 0 && graph.edges.length === 0) {
      return <Loader/>;
    }

    const styledNodes: Node[] = graph.nodes.map((node) => ({
      ...node,
      type: 'graphNode',
      draggable: true,
      data: {
        ...node.data,
        courseStatusMap
      }
    }));

    const styledEdges: Edge[] = graph.edges.map((edge) => ({
      ...edge,
      type: 'graphEdge',
      data: {
        courseStatusMap
      }
    }));

    return (
        <ReactFlowProvider>
          <ReactFlow nodes={styledNodes}
                     edges={styledEdges}
                     nodeTypes={nodeTypes}
                     edgeTypes={edgeTypes}
                     nodesDraggable={true}
          />
        </ReactFlowProvider>
    )
  }

  return (
      <div className={styles.explore} style={{width: '100%', height: '1000px'}}>
        <button className={styles.sidebarButton}
                onClick={() => toggleSidebar()}>{'☰'}</button>
        {renderContents()}
      </div>
  )
}

export default Explore;