from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from app.repositories.course_repo import CourseRepository

class CourseGraphService:

    @staticmethod
    def get_graph(db: Session, course):
        nodes = []
        edges = []
        queue = [course]

        index = 0
        edge_number = 1
        while queue:
            data = CourseRepository.get_course_data(db, queue.pop())

            node = {
                'id': data['course'].replace(' ', ''),
                'data': data,
                'position': {0, index * 100}
            }
            index += 1
            nodes.append(node)

            # Add Edges
            next_courses = CourseRepository.get_next_courses(db, node['id'].replace(' ',''))


            for destination in next_courses:
                if node['id'] == destination:
                    continue
                # add the edge
                edge = {
                    'id': f'edge-{edge_number}',
                    'source': node['id'],
                    'target': destination
                }
                edges.append(edge)
                edge_number += 1
                #add the destination node to queue
                queue.append(destination)

        return {
            'nodes': nodes,
            'edges': edges
        }


