import ExploreView from '../ExploreView';

interface Props {
    params: { course: string };
}

export default function ExploreCoursePage({ params }: Props) {
    return <ExploreView initialCourse={params.course} />;
}
