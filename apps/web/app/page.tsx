'use client'

import { useMemo, useState } from 'react'

const sections = ['发布', '素材', '账号', '日志', '设置'] as const
type Section = (typeof sections)[number]

const platforms = [
  { name: '抖音', state: '可发布', tone: 'good', queue: 7 },
  { name: '小红书', state: '需复验', tone: 'warn', queue: 4 },
  { name: '视频号', state: '可发布', tone: 'good', queue: 5 },
  { name: 'B站', state: '未连接', tone: 'muted', queue: 0 }
]

const tasks = [
  { title: '民宿探店 15 秒短视频', channel: '抖音 + 视频号', time: '20:30', status: '待发布' },
  { title: '周末房型图文合集', channel: '小红书', time: '21:10', status: '待复核' },
  { title: '客户评价剪辑版', channel: '抖音', time: '明天 09:00', status: '草稿' }
]

const assets = [
  { type: '视频', name: 'room-tour-final.mp4', meta: '42s / 1080p' },
  { type: '图文', name: 'may-stay-notes.md', meta: '8 图 / 620 字' },
  { type: '封面', name: 'cover-lake-view.png', meta: '3:4' }
]

const logs = [
  '20:11 生成发布任务草稿',
  '20:12 检查 3 个平台账号状态',
  '20:13 小红书登录态需要复验',
  '20:14 抖音标题通过长度检查'
]

export default function Home() {
  const [activeSection, setActiveSection] = useState<Section>('发布')
  const [selectedPlatforms, setSelectedPlatforms] = useState(['抖音', '视频号'])
  const [notice, setNotice] = useState('已载入今日发布工作台')
  const [draftCount, setDraftCount] = useState(16)

  const selectedLabel = useMemo(
    () => selectedPlatforms.length > 0 ? selectedPlatforms.join(' + ') : '未选择平台',
    [selectedPlatforms]
  )

  function togglePlatform(name: string) {
    setSelectedPlatforms((current) => {
      const next = current.includes(name)
        ? current.filter((item) => item !== name)
        : [...current, name]
      setNotice(next.length > 0 ? `已选择 ${next.join(' + ')}` : '请至少选择一个发布平台')
      return next
    })
  }

  function createTask() {
    setDraftCount((count) => count + 1)
    setActiveSection('发布')
    setNotice('已创建一个新的发布任务草稿')
  }

  function syncAccounts() {
    setNotice('账号状态已刷新：小红书仍需复验')
  }

  return (
    <main className="app-shell">
      <aside className="rail" aria-label="主导航">
        <div className="brand">
          <span className="brand-mark">MP</span>
          <span>Matrix</span>
        </div>
        <nav className="nav-list">
          {sections.map((section) => (
            <button
              className={`nav-item ${activeSection === section ? 'active' : ''}`}
              key={section}
              onClick={() => {
                setActiveSection(section)
                setNotice(`已切换到${section}`)
              }}
              type="button"
            >
              {section}
            </button>
          ))}
        </nav>
        <div className="rail-meter">
          <span>今日进度</span>
          <strong>12 / 18</strong>
          <div className="meter-track"><span /></div>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">多平台发布中控</p>
            <h1>{sectionTitle(activeSection)}</h1>
          </div>
          <div className="top-actions">
            <button className="icon-button" aria-label="同步账号" onClick={syncAccounts} type="button">↻</button>
            <button className="primary-action" onClick={createTask} type="button">新建发布任务</button>
          </div>
        </header>

        <div className="notice-bar" role="status">{notice}</div>

        {activeSection === '发布' && (
          <>
            <section className="command-strip" aria-label="发布概览">
              <div>
                <span className="metric-label">可发布账号</span>
                <strong>9</strong>
              </div>
              <div>
                <span className="metric-label">待处理任务</span>
                <strong>{draftCount}</strong>
              </div>
              <div>
                <span className="metric-label">失败重试</span>
                <strong>2</strong>
              </div>
              <div>
                <span className="metric-label">素材就绪率</span>
                <strong>83%</strong>
              </div>
            </section>

            <section className="main-grid">
              <div className="panel composer">
                <div className="panel-heading">
                  <div>
                    <p className="eyebrow">任务编排</p>
                    <h2>发布任务草稿</h2>
                  </div>
                  <span className="status-pill">自动保存</span>
                </div>

                <label className="field">
                  <span>作品标题</span>
                  <input value="湖景房周末入住体验" readOnly />
                </label>

                <label className="field">
                  <span>发布文案</span>
                  <textarea
                    value="把入住动线、窗边视角和早餐服务压缩成 30 秒以内，抖音强调节奏，小红书保留体验细节。"
                    readOnly
                  />
                </label>

                <div className="platform-row">
                  {platforms.map((platform) => (
                    <button
                      className={`platform-chip ${platform.tone} ${selectedPlatforms.includes(platform.name) ? 'selected' : ''}`}
                      key={platform.name}
                      onClick={() => togglePlatform(platform.name)}
                      type="button"
                    >
                      <span>{platform.name}</span>
                      <small>{platform.state}</small>
                    </button>
                  ))}
                </div>

                <div className="schedule-bar">
                  <div>
                    <span className="metric-label">发布时间</span>
                    <strong>今晚 20:30</strong>
                    <small>{selectedLabel}</small>
                  </div>
                  <button className="secondary-action" onClick={() => setNotice(`已生成 ${selectedLabel} 的发布命令预览`)} type="button">
                    预览命令
                  </button>
                </div>
              </div>

              <QueuePanel />
              <PlatformPanel />
              <AssetsPanel />
              <LogsPanel />
            </section>
          </>
        )}

        {activeSection === '素材' && <AssetsWorkspace />}
        {activeSection === '账号' && <AccountsWorkspace />}
        {activeSection === '日志' && <LogsWorkspace />}
        {activeSection === '设置' && <SettingsWorkspace />}
      </section>
    </main>
  )
}

function sectionTitle(section: Section) {
  const titles: Record<Section, string> = {
    发布: '把今天的内容排进正确的平台节奏',
    素材: '先把素材整理成可发布的状态',
    账号: '确认每个平台账号都能执行',
    日志: '看清每一次发布动作',
    设置: '把发布规则固定下来'
  }
  return titles[section]
}

function QueuePanel() {
  return (
    <div className="panel queue">
      <PanelTitle eyebrow="执行队列" title="即将发布" />
      <div className="task-list">
        {tasks.map((task) => (
          <article className="task-card" key={task.title}>
            <div>
              <h3>{task.title}</h3>
              <p>{task.channel}</p>
            </div>
            <div className="task-meta">
              <span>{task.time}</span>
              <strong>{task.status}</strong>
            </div>
          </article>
        ))}
      </div>
    </div>
  )
}

function PlatformPanel() {
  return (
    <div className="panel platform-health">
      <PanelTitle eyebrow="平台状态" title="账号连通性" />
      <div className="health-list">
        {platforms.map((platform) => (
          <div className="health-row" key={platform.name}>
            <span className={`signal ${platform.tone}`} />
            <span>{platform.name}</span>
            <strong>{platform.queue}</strong>
          </div>
        ))}
      </div>
    </div>
  )
}

function AssetsPanel() {
  return (
    <div className="panel assets">
      <PanelTitle eyebrow="素材库" title="已选素材" />
      <AssetList />
    </div>
  )
}

function LogsPanel() {
  return (
    <div className="panel log-panel">
      <PanelTitle eyebrow="执行日志" title="最近动作" />
      <LogList />
    </div>
  )
}

function AssetsWorkspace() {
  return (
    <section className="workspace-grid">
      <div className="panel wide-panel">
        <PanelTitle eyebrow="素材治理" title="素材入库" />
        <div className="asset-drop">
          <strong>拖入视频、图文或封面</strong>
          <span>自动识别格式、比例、标题候选和可发布平台</span>
        </div>
      </div>
      <div className="panel">
        <PanelTitle eyebrow="当前素材" title="待处理" />
        <AssetList />
      </div>
    </section>
  )
}

function AccountsWorkspace() {
  return (
    <section className="workspace-grid">
      {platforms.map((platform) => (
        <div className="panel account-panel" key={platform.name}>
          <div className="account-head">
            <span className={`signal ${platform.tone}`} />
            <h2>{platform.name}</h2>
          </div>
          <p>{platform.state}</p>
          <button className="secondary-action" type="button">检查登录态</button>
        </div>
      ))}
    </section>
  )
}

function LogsWorkspace() {
  return (
    <section className="workspace-grid">
      <div className="panel wide-panel">
        <PanelTitle eyebrow="发布链路" title="执行日志" />
        <LogList />
      </div>
      <div className="panel">
        <PanelTitle eyebrow="异常" title="待重试" />
        <article className="task-card">
          <div>
            <h3>小红书登录态失效</h3>
            <p>需要重新打开浏览器完成验证</p>
          </div>
          <strong>待处理</strong>
        </article>
      </div>
    </section>
  )
}

function SettingsWorkspace() {
  return (
    <section className="workspace-grid">
      <div className="panel wide-panel">
        <PanelTitle eyebrow="发布规则" title="默认策略" />
        <div className="settings-list">
          <label><input type="checkbox" defaultChecked /> 发布前检查账号登录态</label>
          <label><input type="checkbox" defaultChecked /> 失败平台单独重试</label>
          <label><input type="checkbox" /> 发布后自动生成复盘摘要</label>
        </div>
      </div>
      <div className="panel">
        <PanelTitle eyebrow="服务" title="Python API" />
        <p className="muted-copy">http://127.0.0.1:8787</p>
        <button className="secondary-action" type="button">测试连接</button>
      </div>
    </section>
  )
}

function PanelTitle({ eyebrow, title }: { eyebrow: string; title: string }) {
  return (
    <div className="panel-heading">
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
      </div>
    </div>
  )
}

function AssetList() {
  return (
    <div className="asset-list">
      {assets.map((asset) => (
        <article className="asset-card" key={asset.name}>
          <span>{asset.type}</span>
          <div>
            <h3>{asset.name}</h3>
            <p>{asset.meta}</p>
          </div>
        </article>
      ))}
    </div>
  )
}

function LogList() {
  return (
    <ol className="log-list">
      {logs.map((log) => (
        <li key={log}>{log}</li>
      ))}
    </ol>
  )
}
