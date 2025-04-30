'use client';

import ReactFlow, {Node, Edge, MarkerType, ReactFlowProvider} from 'reactflow';
import 'reactflow/dist/style.css';
import {JSX, useEffect, useState} from "react";
import '../globals.css';
import axios from 'axios';
import CourseNode from "@/app/components/flow/CourseNode/CourseNode";
import CourseEdge from "@/app/components/flow/CourseEdge/CourseEdge";
import styles from './playground.module.css'

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


const Playground = (): JSX.Element  => {

  const [coursesTaken, setCoursesTaken] = useState(new Set());

  const [courseStatusMap, setCourseStatusMap] = useState<CourseStatusMap>(new Map());

  const [graph, setGraph] = useState<{
    nodes: Node[];
    edges: Edge[];
  }>({ nodes: [], edges: [] });

  useEffect(() => {
    const updateGraph = async () => {
      try {
        const course = 'CS2500';
        const url = `${BASE_URL}/api/graph/course/${course}`;
        const response = await axios.get(url);
        setGraph(response.data);

      } catch (error) {
        console.error(error);
      }
    }
    updateGraph()
    setCoursesTaken(new Set())
  },[])

  useEffect(() => {
    const updateCourseStatusMap = async () => {
      try {
        const courses = graph.nodes.map(node => node.data.course.replace(/\s+/g, ''));
        console.log('Courses taken: '+Array.from(coursesTaken));
        const url = `${BASE_URL}/api/course/check`;
        const response = await axios.post(url, {
          coursesTaken: Array.from(coursesTaken),
          courses: courses
        });

        setCourseStatusMap(new Map(Object.entries(response.data)));
        console.log('[Course Status Map Check:]')
        console.log(courseStatusMap)
      } catch (error) {
        console.error(error);
      }
    }
    updateCourseStatusMap();
  }, [coursesTaken, graph]);


  if (graph.nodes.length === 0 && graph.edges.length === 0) {
      return (
          <h1>Fetching Graph</h1>
      )
  }

  const styledNodes: Node[] = graph.nodes.map((node) => ({
    ...node,
    type: 'graphNode',
    draggable: true,
    data: {
      ...node.data,
      coursesTaken,
      setCoursesTaken,
      courseStatusMap
    }
  }));

  const styledEdges: Edge[] = graph.edges.map((edge) => ({
    ...edge,
    type: 'graphEdge',
    data: {
      coursesTaken,
      courseStatusMap
    }
  }));

  return (
      <div className={styles.playground} style={{width: '100%', height: '1000px'}}>
        <ReactFlowProvider>
          <ReactFlow nodes={styledNodes}
                     edges={styledEdges}
                     nodeTypes={nodeTypes}
                     edgeTypes={edgeTypes}
                     nodesDraggable={true}
          />
        </ReactFlowProvider>
      </div>
  )
}

export default Playground;