import {requireChatGPTUser} from '@/app/chatgpt-auth';
import Workspace from '../development/workspace';
export const dynamic='force-dynamic';
export default async function Page(){await requireChatGPTUser('/learning');return <Workspace mode="learning"/>;}
