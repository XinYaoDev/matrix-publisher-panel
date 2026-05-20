/** 支持的平台标识 */
export type PlatformId = 'douyin' | 'xiaohongshu' | 'shipinhao'

/** 平台元信息 */
export interface PlatformInfo {
  id: PlatformId
  name: string
  command: string
}

/** 平台账号 */
export interface PlatformAccount {
  id: string
  platform: PlatformId
  alias: string
  loginName: string
  groupId: string
}
