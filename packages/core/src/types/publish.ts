/** 发布状态 */
export type PublishStatus = 'ready' | 'running' | 'success' | 'failed' | 'cancelled'

/** 作品类型 */
export type WorkType = 'video' | 'note'

/** 作品 */
export interface Work {
  id: string
  type: WorkType
  title: string
  desc: string
  tags: string
  videoPath: string
  imagePaths: string
}

/** 发布任务 */
export interface PublishTask {
  id: string
  workId: string
  accountId: string
  platform: string
  status: PublishStatus
  command: string
  createdAt: string
  updatedAt: string
}

/** 账号分组 */
export interface AccountGroup {
  id: string
  name: string
  workId: string
}

/** API 错误类型 */
export type ErrorType = 'NETWORK' | 'AUTH' | 'VALIDATION' | 'PLATFORM' | 'UNKNOWN'

/** API 响应 */
export interface ApiResponse<T = unknown> {
  ok: boolean
  data?: T
  error?: {
    type: ErrorType
    message: string
    details?: unknown
  }
}
