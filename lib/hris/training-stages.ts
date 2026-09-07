import type {DevelopmentRecord as R} from './development';
export function previousTrainingStagesCompleted(training:R,records:R[],employeeId:string,courseId:string){
 const stages=training.payload.trainingStages??[];
 if(!stages.length)return true;
 const index=stages.findIndex(stage=>stage.courseIds.includes(courseId));
 return index>=0&&stages.slice(0,index).flatMap(stage=>stage.courseIds).every(id=>records.some(r=>r.kind==='enrollment'&&r.employeeId===employeeId&&r.payload.trainingId===training.id&&r.referenceId===id&&r.status==='completed'));
}
