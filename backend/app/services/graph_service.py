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


        while queue:
            data = CourseRepository.get_course_data(db, queue.pop())

            node = {
                'id': data['course'],
                'data': data,
                'position': {0, index * 100}
            }
            index += 1
            nodes.append(node)

            # Add Edges
            for destination in CourseRepository.get_next_courses(db, node['id']):
                # add the edge
                edge = {
                    'id': f'edge-{index}',
                    'source': node['id'],
                    'target': course
                }
                edges.append(edge)
                #add the destination node to queue
                queue.append(destination)

        return {
            'nodes': nodes,
            'edges': edges
        }


