'use client';

import ReactFlow, {Node, Edge, ReactFlowProvider} from 'reactflow';
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
import styles from './explore.module.css'



const nodeTypes = {
  graphNode: CourseNode
};

const edgeTypes = {
  graphEdge: CourseEdge,
};


export type CourseStatus = {
  satisfied: boolean;
  message: string;
};

export type CourseStatusMap = Map<string, CourseStatus>;





const Explore = (): JSX.Element  => {

  // Zustand Shared State
  const source: string = useGraphStore((s) => s.source);
  const coursesTaken = useUserDataStore((s) => s.coursesTaken);
  // Filters
  const departments: Set<string> = useCourseFilterStore((s) => s.departments);
  const minCourseID: number = useCourseFilterStore((s) => s.minCourseID);
  const maxCourseID: number = useCourseFilterStore((s) => s.maxCourseID);
  const attributes: string[] = useCourseFilterStore((s) => s.attributes);


  const [courseStatusMap, setCourseStatusMap] = useState<CourseStatusMap>(new Map());
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const [graph, setGraph] = useState<{
    nodes: Node[];
    edges: Edge[];
  }>({ nodes: [], edges: [] });

  useEffect(() => {
    const updateGraph = async () => {
      if (source === '') return;
      try {
        const url = `${BASE_URL}/api/graph/course/${source}`;
        console.log('min: '+minCourseID);
        console.log('max = '+maxCourseID);
        console.log('POST BEING MADE WITH '+source);
        const response = await axios.post(url, {
          departments: Array.from(departments),
          minCourseID: minCourseID,
          maxCourseID: maxCourseID,
          attributes: attributes
        });

        setGraph(response.data);
      } catch (error) {
        console.error(error);
      }
    }
    updateGraph()
  },[source, departments, minCourseID, maxCourseID, attributes])

  useEffect(() => {
    const updateCourseStatusMap = async () => {
      if (graph.nodes === undefined || graph.nodes.length === 0) {
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
      if (source === '') {
          return (
              <div className={styles.emptyState}>
                  <svg
                      viewBox="0 0 24 24"
                      aria-hidden="true"
                      className={styles.icon}
                  >
                    <path
                        d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18.4A8.4 8.4 0 1 1 20.4 12 8.41 8.41 0 0 1 12 20.4zm2.8-12.3-2.5 7.1-7.1 2.5 2.5-7.1 7.1-2.5z"></path>
                  </svg>

                  <h2>Select a course to begin</h2>
                  <p className={styles.helpText}>
                      Use the sidebar search to choose a root&nbsp;course.<br/>
                      The prerequisite graph will appear here.
                  </p>
              </div>
        )
      }

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
                       style={{ width: '100%', height: '100%' }}
            />
          </ReactFlowProvider>
      )
  }

  return (
      <div className={styles.exploreContainer}>

        {sidebarOpen && <Sidebar/>}
        <div className={styles.explore}>
          <button className={styles.sidebarButton}
                  onClick={() => setSidebarOpen(prev => !prev)}>{'☰'}</button>
          {renderContents()}
        </div>
      </div>
  )
}

export default Explore;