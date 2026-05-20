import type { PlatformInfo } from '../types'

/** 支持的平台列表 */
export const PLATFORMS: PlatformInfo[] = [
  { id: 'douyin', name: '抖音', command: 'douyin' },
  { id: 'xiaohongshu', name: '小红书', command: 'xiaohongshu' },
  { id: 'shipinhao', name: '视频号', command: 'tencent' }
]

/** 默认后端 API 基础路径 */
export const API_BASE_URL = 'http://localhost:8080/api'
