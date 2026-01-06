from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QWidget, QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtCore import Qt, QPointF
import sys
import math


class TargetPlotter:
    def __init__(self, scene):
        self.scene = scene
        self.targets_A = {}
        self.targets_B = {}

    def polar_to_cartesian(self, range_val, azimuth_deg):
        angle_rad = math.radians(azimuth_deg)
        x = range_val * math.cos(angle_rad)
        y = -range_val * math.sin(angle_rad)  # Negative Y for top-down display
        return x, y

    def create_target_item(self, target):
        x, y = self.polar_to_cartesian(target['range'], target['azimuth'])
        dot = QGraphicsEllipseItem(-4, -4, 8, 8)
        dot.setBrush(QBrush(QColor("red") if target['category'] == 'A' else QColor("blue")))
        dot.setPos(x, y)
        dot.setZValue(1)
        return dot

    def update_targets(self, targets):
        # Clear existing items
        for item in self.targets_A.values():
            self.scene.removeItem(item)
        for item in self.targets_B.values():
            self.scene.removeItem(item)
        self.targets_A.clear()
        self.targets_B.clear()

        # Add new items
        for t in targets:
            item = self.create_target_item(t)
            if t['category'] == 'A':
                self.targets_A[t['id']] = item
            else:
                self.targets_B[t['id']] = item
            self.scene.addItem(item)

    def show_targets(self, category, visible):
        group = self.targets_A if category == 'A' else self.targets_B
        for item in group.values():
            item.setVisible(visible)

    def show_all(self, visible=True):
        for item in self.targets_A.values():
            item.setVisible(visible)
        for item in self.targets_B.values():
            item.setVisible(visible)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polar Display - Target Categories")
        self.setGeometry(200, 200, 800, 600)

        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Graphics view/scene
        self.scene = QGraphicsScene(-300, -300, 600, 600)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        main_layout.addWidget(self.view)

        # Buttons
        button_layout = QHBoxLayout()
        self.btn_cat_a = QPushButton("Show Category A")
        self.btn_cat_b = QPushButton("Show Category B")
        self.btn_both = QPushButton("Show Both")
        button_layout.addWidget(self.btn_cat_a)
        button_layout.addWidget(self.btn_cat_b)
        button_layout.addWidget(self.btn_both)
        main_layout.addLayout(button_layout)

        # Plotter
        self.target_plotter = TargetPlotter(self.scene)

        # Button connections
        self.btn_cat_a.clicked.connect(lambda: self.show_category('A'))
        self.btn_cat_b.clicked.connect(lambda: self.show_category('B'))
        self.btn_both.clicked.connect(lambda: self.show_category('Both'))

        # Mock data
        self.load_mock_targets()

    def show_category(self, cat):
        if cat == 'A':
            self.target_plotter.show_targets('A', True)
            self.target_plotter.show_targets('B', False)
        elif cat == 'B':
            self.target_plotter.show_targets('A', False)
            self.target_plotter.show_targets('B', True)
        elif cat == 'Both':
            self.target_plotter.show_all(True)

    def load_mock_targets(self):
        targets = []
        for i in range(10):
            targets.append({'id': f'A{i}', 'range': 50 + i*10, 'azimuth': i * 10, 'category': 'A'})
        for i in range(10):
            targets.append({'id': f'B{i}', 'range': 60 + i*10, 'azimuth': i * 15 + 5, 'category': 'B'})
        self.target_plotter.update_targets(targets)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

# https://1drv.ms/w/c/fd9c3d82ca06da8b/EbNd5EqlnKlEr2a-YnFYdLkBcDS9DQJw4vcILXQy2tzNig?e=un3PCJ
# https://1drv.ms/w/c/fd9c3d82ca06da8b/Ed2G0R9g5YVGrBB-oZjEpNABxur3pGtAphdJd7wSkxXyWA?e=KdZsqm

"""
MyApp.cpp
#include "pch.h"
#include "MyApp.h"
#include "MyDlg.h"

CMyApp theApp;

BOOL CMyApp::InitInstance()
{
    CWinApp::InitInstance();

    CMyDlg dlg;
    m_pMainWnd = &dlg;
    dlg.DoModal();

    return FALSE;
}

.h
#pragma once
#include "resource.h"

class CMyApp : public CWinApp
{
public:
    virtual BOOL InitInstance();
};

extern CMyApp theApp;

MyDlg.cpp
#include "pch.h"
#include "MyApp.h"
#include "MyDlg.h"

IMPLEMENT_DYNAMIC(CMyDlg, CDialogEx)

CMyDlg::CMyDlg(CWnd* pParent)
    : CDialogEx(IDD_MY_DIALOG, pParent)
{
}

void CMyDlg::DoDataExchange(CDataExchange* pDX)
{
    CDialogEx::DoDataExchange(pDX);
    DDX_Text(pDX, IDC_EDIT1, m_editText);
}

BEGIN_MESSAGE_MAP(CMyDlg, CDialogEx)
    ON_BN_CLICKED(IDC_BUTTON_ADD, &CMyDlg::OnBnClickedAdd)
    ON_WM_DESTROY()
END_MESSAGE_MAP()

BOOL CMyDlg::OnInitDialog()
{
    CDialogEx::OnInitDialog();

    InitializeCriticalSection(&g_cs);
    g_wakeEvent.Create(FALSE, FALSE, nullptr);

    AfxBeginThread(ExpiryThreadProc, nullptr);

    return TRUE;
}

void CMyDlg::OnBnClickedAdd()
{
    UpdateData(TRUE);

    Item item;
    item.name = m_editText;
    item.expiry = CTime::GetCurrentTime() + CTimeSpan(0, 0, 0, 10);

    EnterCriticalSection(&g_cs);
    g_items.push_back(item);   // FIFO
    LeaveCriticalSection(&g_cs);

    g_wakeEvent.SetEvent();    // wake worker
}

void CMyDlg::OnDestroy()
{
    CDialogEx::OnDestroy();

    EnterCriticalSection(&g_cs);
    g_stopThread = true;
    LeaveCriticalSection(&g_cs);

    g_wakeEvent.SetEvent();
    Sleep(100);

    DeleteCriticalSection(&g_cs);
}

MyDlg.h

#pragma once
#include "resource.h"
#include "Globals.h"

class CMyDlg : public CDialogEx
{
public:
    CMyDlg(CWnd* pParent = nullptr);

#ifdef AFX_DESIGN_TIME
    enum { IDD = IDD_MY_DIALOG };
#endif

protected:
    virtual void DoDataExchange(CDataExchange* pDX);
    virtual BOOL OnInitDialog();
    afx_msg void OnDestroy();
    afx_msg void OnBnClickedAdd();

    DECLARE_MESSAGE_MAP()

private:
    CString m_editText;
};

ExpiryThread.cpp
#include "Globals.h"

UINT ExpiryThreadProc(LPVOID)
{
    while (true)
    {
        DWORD waitMs = INFINITE;

        EnterCriticalSection(&g_cs);

        if (g_stopThread)
        {
            LeaveCriticalSection(&g_cs);
            break;
        }

        if (!g_items.empty())
        {
            CTime now = CTime::GetCurrentTime();
            CTime expiry = g_items.front().expiry;

            if (expiry <= now)
            {
                g_items.pop_front();   // remove oldest
                LeaveCriticalSection(&g_cs);
                continue;
            }

            waitMs = (DWORD)((expiry - now).GetTotalSeconds() * 1000);
        }

        LeaveCriticalSection(&g_cs);

        // wait until expiry or until new item added
        g_wakeEvent.Lock(waitMs);
        g_wakeEvent.ResetEvent();
    }

    return 0;
}

Globals.cpp
#include "Globals.h"

std::deque<Item> g_items;

CRITICAL_SECTION g_cs;
CEvent g_wakeEvent;
bool g_stopThread = false;

Globals.h

#pragma once
#include <deque>
#include "Item.h"

extern std::deque<Item> g_items;

extern CRITICAL_SECTION g_cs;
extern CEvent g_wakeEvent;
extern bool g_stopThread;

UINT ExpiryThreadProc(LPVOID);

Item.h

#pragma once
#include <afx.h>

struct Item
{
    CString name;
    CTime   expiry;
};
"""


"""
Item.h
#pragma once
#include <afx.h>   // CTime

struct Item
{
    CTime expiry;
};


WorkerThread.h
#pragma once

#include <deque>
#include <windows.h>
#include "Item.h"

// Shared objects
extern std::deque<Item> g_items;
extern CRITICAL_SECTION g_cs;
extern HANDLE g_hWakeEvent;
extern bool g_exitThread;

// Worker thread procedure
UINT WorkerThreadProc(LPVOID pParam);


WorkerThread.cpp
#include "WorkerThread.h"

// Globals
std::deque<Item> g_items;
CRITICAL_SECTION g_cs;
HANDLE g_hWakeEvent = nullptr;
bool g_exitThread = false;

UINT WorkerThreadProc(LPVOID)
{
    while (!g_exitThread)
    {
        // Wake every 1 second or when signaled
        WaitForSingleObject(g_hWakeEvent, 1000);

        EnterCriticalSection(&g_cs);

        if (!g_items.empty())
        {
            CTime now = CTime::GetCurrentTime();

            // Remove all expired items (oldest first)
            while (!g_items.empty() &&
                   g_items.front().expiry <= now)
            {
                g_items.pop_front();
            }
        }

        ResetEvent(g_hWakeEvent);
        LeaveCriticalSection(&g_cs);
    }

    return 0;
}



MyDlg.h
#pragma once

#include <afxwin.h>

class CMyDlg : public CDialogEx
{
public:
    CMyDlg();

protected:
    virtual BOOL OnInitDialog();
    afx_msg void OnAddButton();
    virtual void OnCancel();

    DECLARE_MESSAGE_MAP()

private:
    CWinThread* m_pWorkerThread;
};



MyDlg.cpp
#include "MyDlg.h"
#include "WorkerThread.h"

BEGIN_MESSAGE_MAP(CMyDlg, CDialogEx)
    ON_BN_CLICKED(IDC_ADD_BUTTON, &CMyDlg::OnAddButton)
END_MESSAGE_MAP()

CMyDlg::CMyDlg()
    : CDialogEx(IDD_MY_DIALOG),
      m_pWorkerThread(nullptr)
{
}

BOOL CMyDlg::OnInitDialog()
{
    CDialogEx::OnInitDialog();

    // Initialize synchronization
    InitializeCriticalSection(&g_cs);
    g_hWakeEvent = CreateEvent(nullptr, TRUE, FALSE, nullptr);

    // Start worker thread ONCE
    m_pWorkerThread = AfxBeginThread(WorkerThreadProc, nullptr);

    return TRUE;
}


void CMyDlg::OnAddButton()
{
    Item item;
    item.expiry = CTime::GetCurrentTime() + CTimeSpan(0, 0, 0, 10); // +10 sec

    EnterCriticalSection(&g_cs);
    g_items.push_back(item);   // ordered insertion
    LeaveCriticalSection(&g_cs);

    // Wake worker thread immediately
    SetEvent(g_hWakeEvent);
}

void CMyDlg::OnCancel()
{
    // Signal thread to exit
    g_exitThread = true;
    SetEvent(g_hWakeEvent);

    if (m_pWorkerThread)
    {
        WaitForSingleObject(m_pWorkerThread->m_hThread, INFINITE);
    }

    CloseHandle(g_hWakeEvent);
    DeleteCriticalSection(&g_cs);

    CDialogEx::OnCancel();
}





















"""
