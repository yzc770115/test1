using UnityEngine;
using System.Collections.Generic;

public class TetrisGame : MonoBehaviour
{
    // 常量定义
    private const int GRID_WIDTH = 10;
    private const int GRID_HEIGHT = 20;
    private const float CELL_SIZE = 1.0f; // Unity单位

    // 形状定义
    private static readonly Dictionary<string, int[][,]> SHAPES = new Dictionary<string, int[][,]>
    {
        {
            "I", new int[][,] {
                new int[,] {
                    {0, 0, 0, 0},
                    {1, 1, 1, 1},
                    {0, 0, 0, 0},
                    {0, 0, 0, 0}
                },
                new int[,] {
                    {0, 0, 1, 0},
                    {0, 0, 1, 0},
                    {0, 0, 1, 0},
                    {0, 0, 1, 0}
                },
                new int[,] {
                    {0, 0, 0, 0},
                    {0, 0, 0, 0},
                    {1, 1, 1, 1},
                    {0, 0, 0, 0}
                },
                new int[,] {
                    {0, 1, 0, 0},
                    {0, 1, 0, 0},
                    {0, 1, 0, 0},
                    {0, 1, 0, 0}
                }
            }
        },
        {
            "O", new int[][,] {
                new int[,] {
                    {1, 1},
                    {1, 1}
                }
            }
        },
        {
            "T", new int[][,] {
                new int[,] {
                    {0, 1, 0},
                    {1, 1, 1},
                    {0, 0, 0}
                },
                new int[,] {
                    {0, 1, 0},
                    {0, 1, 1},
                    {0, 1, 0}
                },
                new int[,] {
                    {0, 0, 0},
                    {1, 1, 1},
                    {0, 1, 0}
                },
                new int[,] {
                    {0, 1, 0},
                    {1, 1, 0},
                    {0, 1, 0}
                }
            }
        },
        // 其他形状类似...
    };

    // 形状颜色定义
    private static readonly Dictionary<string, int> SHAPE_COLORS = new Dictionary<string, int>
    {
        { "I", 0 }, // 青色
        { "O", 1 }, // 黄色
        { "T", 2 }, // 紫色
        { "L", 3 }, // 橙色
        { "J", 4 }, // 蓝色
        { "S", 5 }, // 绿色
        { "Z", 6 }  // 红色
    };

    // 游戏状态
    private enum GameState
    {
        Menu,
        Playing,
        GameOver,
        LevelComplete
    }

    // 成员变量
    private GameState currentState;
    private string[,] board;
    private string currentShape;
    private int currentRotation;
    private Vector2Int currentPosition;
    private string nextShape;
    private float lastFallTime;
    private float fallSpeed = 1.0f;
    private int score = 0;
    private int level = 1;

    // Unity组件引用
    [SerializeField] private GameObject blockPrefab;
    [SerializeField] private Transform boardContainer;
    private Dictionary<Vector2Int, GameObject> blockObjects;

    private void Start()
    {
        InitializeGame();
    }

    private void InitializeGame()
    {
        board = new string[GRID_HEIGHT, GRID_WIDTH];
        blockObjects = new Dictionary<Vector2Int, GameObject>();
        currentState = GameState.Playing;
        score = 0;
        level = 1;
        
        // 生成第一个方块
        SpawnNewPiece();
    }

    private void Update()
    {
        if (currentState != GameState.Playing) return;

        HandleInput();
        HandleFalling();
    }

    private void HandleInput()
    {
        if (Input.GetKeyDown(KeyCode.LeftArrow))
            TryMove(Vector2Int.left);
        else if (Input.GetKeyDown(KeyCode.RightArrow))
            TryMove(Vector2Int.right);
        else if (Input.GetKeyDown(KeyCode.DownArrow))
            TryMove(Vector2Int.down);
        else if (Input.GetKeyDown(KeyCode.UpArrow))
            TryRotate();
        else if (Input.GetKeyDown(KeyCode.Space))
            HardDrop();
    }

    private void HandleFalling()
    {
        if (Time.time - lastFallTime >= fallSpeed)
        {
            lastFallTime = Time.time;
            if (!TryMove(Vector2Int.down))
            {
                LockPiece();
                ClearLines();
                SpawnNewPiece();
            }
        }
    }

    private bool TryMove(Vector2Int movement)
    {
        Vector2Int newPos = currentPosition + movement;
        if (!CheckCollision(currentShape, currentRotation, newPos))
        {
            currentPosition = newPos;
            UpdatePieceVisual();
            return true;
        }
        return false;
    }

    private void UpdatePieceVisual()
    {
        // 清除所有现有的方块
        foreach (var blockObj in blockObjects.Values)
        {
            Destroy(blockObj);
        }
        blockObjects.Clear();

        // 创建新的方块
        var piece = SHAPES[currentShape][currentRotation];
        for (int y = 0; y < piece.GetLength(0); y++)
        {
            for (int x = 0; x < piece.GetLength(1); x++)
            {
                if (piece[y, x] == 1)
                {
                    Vector2Int pos = new Vector2Int(currentPosition.x + x, currentPosition.y + y);
                    CreateBlock(pos, SHAPE_COLORS[currentShape]);
                }
            }
        }
    }

    private void CreateBlock(Vector2Int position, int colorIndex)
    {
        Vector3 worldPos = new Vector3(
            position.x * CELL_SIZE,
            position.y * CELL_SIZE,
            0
        );

        GameObject blockObj = Instantiate(blockPrefab, worldPos, Quaternion.identity, boardContainer);
        Block block = blockObj.GetComponent<Block>();
        block.SetColor(colorIndex);
        
        blockObjects[position] = blockObj;
    }

    // 其他必要的方法将在后续实现...
} 