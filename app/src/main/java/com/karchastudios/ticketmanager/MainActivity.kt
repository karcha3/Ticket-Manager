package com.karchastudios.ticketmanager

import android.app.Application
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.room.*
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

// ---------- Data (stored only on this phone, in a local Room/SQLite database) ----------

@Entity(tableName = "tickets")
data class Ticket(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val firstName: String = "",
    val lastName: String = "",
    val venueType: String = "Concert",
    val ticketType: String = "Standard",
    val venue: String = "",
    val location: String = "",
    val date: String = "",
    val time: String = "",
    val seat: String = "",
    val price: Double = 0.0,
    val status: String = "Active",
    val notes: String = ""
)

@Dao
interface TicketDao {
    @Query("SELECT * FROM tickets ORDER BY date, time")
    fun all(): Flow<List<Ticket>>
    @Insert suspend fun insert(t: Ticket): Long
    @Update suspend fun update(t: Ticket)
    @Delete suspend fun delete(t: Ticket)
}

@Database(entities = [Ticket::class], version = 1, exportSchema = false)
abstract class AppDb : RoomDatabase() {
    abstract fun dao(): TicketDao
    companion object {
        @Volatile private var instance: AppDb? = null
        fun get(c: android.content.Context): AppDb = instance ?: synchronized(this) {
            instance ?: Room.databaseBuilder(c.applicationContext, AppDb::class.java, "tickets.db")
                .build().also { instance = it }
        }
    }
}

class TicketVm(app: Application) : AndroidViewModel(app) {
    private val dao = AppDb.get(app).dao()
    val tickets = dao.all().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())
    fun save(t: Ticket) { viewModelScope.launch { if (t.id == 0L) dao.insert(t) else dao.update(t) } }
    fun delete(t: Ticket) { viewModelScope.launch { dao.delete(t) } }
}

val VENUE_TYPES = listOf("Concert", "Theater", "Sports", "Conference", "Cinema", "Festival", "Exhibition", "Comedy Show", "Other")
val TICKET_TYPES = listOf("Standard", "VIP", "Early Bird", "Group", "Student", "Season Pass", "Backstage", "Other")
val STATUSES = listOf("Active", "Used", "Cancelled", "Refunded")

private fun money(d: Double) = "\$" + "%.2f".format(d)

private fun Ticket.searchText() = listOf(firstName, lastName, venueType, ticketType, venue,
    location, date, time, seat, status, notes).joinToString(" ")

private fun toCsv(list: List<Ticket>): String {
    val head = listOf("First Name", "Last Name", "Venue Type", "Ticket Type", "Venue / Event",
        "Location", "Date", "Time", "Seat / Section", "Price", "Status", "Notes")
    fun q(s: String): String {
        // A leading = + - @ could run as a formula in Excel, so neutralise it.
        val safe = if (s.isNotEmpty() && s[0] in "=+-@") "'$s" else s
        return "\"" + safe.replace("\"", "\"\"") + "\""
    }
    val rows = list.map { t ->
        listOf(t.firstName, t.lastName, t.venueType, t.ticketType, t.venue, t.location, t.date,
            t.time, t.seat, "%.2f".format(t.price), t.status, t.notes).joinToString(",") { q(it) }
    }
    return (listOf(head.joinToString(",")) + rows).joinToString("\r\n")
}

// ---------- UI ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent { TicketTheme { Surface(Modifier.fillMaxSize()) { AppScreen() } } }
    }
}

@Composable
fun TicketTheme(content: @Composable () -> Unit) {
    val colors = if (isSystemInDarkTheme())
        darkColorScheme(primary = Color(0xFF8B93FF), onPrimary = Color(0xFF10122B))
    else
        lightColorScheme(primary = Color(0xFF4F57E8))
    MaterialTheme(colorScheme = colors, content = content)
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppScreen(vm: TicketVm = viewModel()) {
    val context = LocalContext.current
    val all by vm.tickets.collectAsState()
    var query by remember { mutableStateOf("") }
    var selected by remember { mutableStateOf("All Venues") }
    var form by remember { mutableStateOf<Ticket?>(null) }
    var toDelete by remember { mutableStateOf<Ticket?>(null) }

    val venues = listOf("All Venues") + all.map { it.venue }.filter { it.isNotBlank() }.distinct().sorted()
    val tab = if (selected in venues) selected else "All Venues"
    val shown = all.filter { t ->
        (tab == "All Venues" || t.venue == tab) &&
            (query.isBlank() || t.searchText().contains(query.trim(), ignoreCase = true))
    }
    val total = shown.filter { it.status != "Cancelled" && it.status != "Refunded" }.sumOf { it.price }

    val saver = rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("text/csv")) { uri: Uri? ->
        uri?.let { u ->
            context.contentResolver.openOutputStream(u)?.use { it.write(toCsv(shown).toByteArray()) }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Ticket Manager") },
                actions = { TextButton(onClick = { saver.launch("tickets.csv") }) { Text("Export CSV") } }
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(onClick = { form = Ticket() }) { Text("+ Add ticket") }
        },
        bottomBar = {
            Surface(Modifier.fillMaxWidth(), tonalElevation = 3.dp) {
                Text(
                    "${shown.size} tickets in \"$tab\"  •  Active value: ${money(total)}",
                    Modifier.navigationBarsPadding().padding(12.dp),
                    style = MaterialTheme.typography.bodySmall
                )
            }
        }
    ) { pad ->
        Column(Modifier.padding(pad)) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                label = { Text("Search tickets") }, singleLine = true,
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp)
            )
            ScrollableTabRow(selectedTabIndex = venues.indexOf(tab), edgePadding = 8.dp) {
                venues.forEach { v -> Tab(selected = v == tab, onClick = { selected = v }, text = { Text(v) }) }
            }
            if (shown.isEmpty()) {
                Text("No tickets to show. Tap \"+ Add ticket\" to create one.",
                    Modifier.padding(24.dp), color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            LazyColumn(
                contentPadding = PaddingValues(12.dp, 12.dp, 12.dp, 96.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                items(shown, key = { it.id }) { t ->
                    TicketCard(t,
                        onEdit = { form = t },
                        onDuplicate = { form = t.copy(id = 0) },
                        onDelete = { toDelete = t })
                }
            }
        }
    }

    form?.let { f ->
        TicketForm(f, onCancel = { form = null }, onSave = { vm.save(it); form = null })
    }
    toDelete?.let { t ->
        AlertDialog(
            onDismissRequest = { toDelete = null },
            title = { Text("Delete ticket?") },
            text = { Text("${t.firstName} ${t.lastName} – ${t.venue}. This cannot be undone.") },
            confirmButton = { TextButton(onClick = { vm.delete(t); toDelete = null }) { Text("Delete") } },
            dismissButton = { TextButton(onClick = { toDelete = null }) { Text("Cancel") } }
        )
    }
}

@Composable
fun TicketCard(t: Ticket, onEdit: () -> Unit, onDuplicate: () -> Unit, onDelete: () -> Unit) {
    val dim = MaterialTheme.colorScheme.onSurfaceVariant
    val statusColor = when (t.status) {
        "Cancelled", "Refunded" -> MaterialTheme.colorScheme.error
        "Used" -> dim
        else -> MaterialTheme.colorScheme.primary
    }
    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(14.dp)) {
            Text("${t.firstName} ${t.lastName}".trim(), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text(listOf(t.venue, t.location).filter { it.isNotBlank() }.joinToString(" · "))
            Text(listOf(t.date, t.time, t.seat).filter { it.isNotBlank() }.joinToString(" · "), color = dim)
            Text("${t.venueType} · ${t.ticketType}", color = dim)
            if (t.notes.isNotBlank()) Text(t.notes, color = dim)
            Row(Modifier.fillMaxWidth().padding(top = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                Text(money(t.price), fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.weight(1f))
                Text(t.status, color = statusColor, fontWeight = FontWeight.SemiBold)
            }
            Row {
                TextButton(onClick = onEdit) { Text("Edit") }
                TextButton(onClick = onDuplicate) { Text("Duplicate") }
                TextButton(onClick = onDelete) { Text("Delete", color = MaterialTheme.colorScheme.error) }
            }
        }
    }
}

@Composable
fun TicketForm(initial: Ticket, onSave: (Ticket) -> Unit, onCancel: () -> Unit) {
    var t by remember { mutableStateOf(initial) }
    var price by remember { mutableStateOf(if (initial.price == 0.0) "" else initial.price.toString()) }
    val valid = t.venue.isNotBlank() && (t.firstName.isNotBlank() || t.lastName.isNotBlank())
    AlertDialog(
        onDismissRequest = onCancel,
        title = { Text(if (initial.id == 0L) "New ticket" else "Edit ticket") },
        text = {
            Column(Modifier.verticalScroll(rememberScrollState()), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Field("First name", t.firstName) { t = t.copy(firstName = it) }
                Field("Last name", t.lastName) { t = t.copy(lastName = it) }
                Picker("Venue type", t.venueType, VENUE_TYPES) { t = t.copy(venueType = it) }
                Picker("Ticket type", t.ticketType, TICKET_TYPES) { t = t.copy(ticketType = it) }
                Field("Venue / Event", t.venue) { t = t.copy(venue = it) }
                Field("Location", t.location) { t = t.copy(location = it) }
                Field("Date (yyyy-MM-dd)", t.date) { t = t.copy(date = it) }
                Field("Time (HH:mm)", t.time) { t = t.copy(time = it) }
                Field("Seat / Section", t.seat) { t = t.copy(seat = it) }
                Field("Price", price, KeyboardType.Decimal) { price = it }
                Picker("Status", t.status, STATUSES) { t = t.copy(status = it) }
                Field("Notes", t.notes) { t = t.copy(notes = it) }
            }
        },
        confirmButton = {
            TextButton(enabled = valid, onClick = {
                onSave(t.copy(price = price.replace(',', '.').toDoubleOrNull() ?: 0.0))
            }) { Text("Save") }
        },
        dismissButton = { TextButton(onClick = onCancel) { Text("Cancel") } }
    )
}

@Composable
fun Field(label: String, value: String, keyboard: KeyboardType = KeyboardType.Text, onChange: (String) -> Unit) {
    OutlinedTextField(
        value = value, onValueChange = onChange, label = { Text(label) }, singleLine = true,
        modifier = Modifier.fillMaxWidth(), keyboardOptions = KeyboardOptions(keyboardType = keyboard)
    )
}

@Composable
fun Picker(label: String, value: String, options: List<String>, onPick: (String) -> Unit) {
    var open by remember { mutableStateOf(false) }
    Box {
        OutlinedButton(onClick = { open = true }, modifier = Modifier.fillMaxWidth()) { Text("$label: $value") }
        DropdownMenu(expanded = open, onDismissRequest = { open = false }) {
            options.forEach { o -> DropdownMenuItem(text = { Text(o) }, onClick = { onPick(o); open = false }) }
        }
    }
}
